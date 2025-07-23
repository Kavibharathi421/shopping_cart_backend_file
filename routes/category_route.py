from flask import Blueprint, request, jsonify
from models import db, Categories, Products

category_routes = Blueprint('category_routes', __name__)

@category_routes.route('/categories', methods=['POST'])
def create_category():
    data = request.json
    new_category = Categories(
        category_name=data['category_name'],
        description=data['description']
    )
    db.session.add(new_category)
    db.session.commit()
    return jsonify({"message": "Category created successfully"}), 201


@category_routes.route('/categories', methods=['GET'])
def get_all_categories():
    categories = Categories.query.all()
    result = []
    for cat in categories:
        result.append({
            "category_id": cat.category_id,
            "category_name": cat.category_name,
            "description": cat.description
        })
    return jsonify(result), 200


@category_routes.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    category = Categories.query.get_or_404(category_id)
    products = [{
        "product_id": p.product_id,
        "name": p.name,
        "description": p.description,
        "price": str(p.price),
        "stock_qty": p.stock_qty,
        "image_url": p.image_url
    } for p in category.products]

    return jsonify({
        "category_id": category.category_id,
        "category_name": category.category_name,
        "description": category.description,
        "products": products
    })


@category_routes.route('/categories/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = Categories.query.get_or_404(category_id)
    data = request.json
    for field in data:
        setattr(category, field, data[field])
    db.session.commit()
    return jsonify(category.to_dict())


@category_routes.route('/categories/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = Categories.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category and related products deleted successfully"})
