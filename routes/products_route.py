from flask import Blueprint, request, jsonify
from models import db, Products, Categories

product_routes = Blueprint('product_routes', __name__)

@product_routes.route('/products', methods=['POST'])
def create_product():
    data = request.json
    new_product = Products(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        stock_qty=data['stock_qty'],
        image_url=data.get('image_url'),
        category_id=data['category_id']
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product created successfully"}), 201


@product_routes.route('/products', methods=['GET'])
def get_all_products():
    products = Products.query.all()
    result = []
    for p in products:
        result.append({
            "product_id": p.product_id,
            "name": p.name,
            "description": p.description,
            "price": str(p.price),
            "stock_qty": p.stock_qty,
            "image_url": p.image_url,
            "category": {
                "category_id": p.category.category_id,
                "category_name": p.category.category_name
            }
        })
    return jsonify(result), 200


@product_routes.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    p = Products.query.get_or_404(product_id)
    return jsonify({
        "product_id": p.product_id,
        "name": p.name,
        "description": p.description,
        "price": str(p.price),
        "stock_qty": p.stock_qty,
        "image_url": p.image_url,
        "category": {
            "category_id": p.category.category_id,
            "category_name": p.category.category_name
        }
    })


@product_routes.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    p = Products.query.get_or_404(product_id)
    data = request.json

    p.name = data.get('name', p.name)
    p.description = data.get('description', p.description)
    p.price = data.get('price', p.price)
    p.stock_qty = data.get('stock_qty', p.stock_qty)
    p.image_url = data.get('image_url', p.image_url)
    p.category_id = data.get('category_id', p.category_id)

    db.session.commit()
    return jsonify({"message": "Product updated successfully"})


@product_routes.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    p = Products.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"message": "Product deleted successfully"})
