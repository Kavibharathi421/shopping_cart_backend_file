from flask import Blueprint, request, jsonify
from models import db, Cart, Products, Login

cart_routes = Blueprint('cart_routes', __name__)

@cart_routes.route('/cart', methods=['POST'])
def add_to_cart():
    data = request.json
    login_id = data.get('login_id')
    product_id = data.get('product_id')
    quantity = data.get('quantity')

    product = Products.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    user = Login.query.get(login_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    existing_item = Cart.query.filter_by(login_id=login_id, product_id=product_id).first()
    if existing_item:
        existing_item.quantity += quantity
    else:
        new_item = Cart(login_id=login_id, product_id=product_id, quantity=quantity)
        db.session.add(new_item)

    db.session.commit()
    return jsonify({'message': 'Item added to cart'}), 201


@cart_routes.route('/cart/<int:login_id>', methods=['GET'])
def get_cart(login_id):
    items = Cart.query.filter_by(login_id=login_id).all()
    cart_data = []
    for item in items:
        cart_data.append({
            'cart_id': item.cart_id,
            'login_id': item.login_id,
            'product_id': item.product_id,
            'product_name': item.product.name,
            'price': str(item.product.price),
            'quantity': item.quantity
        })
    return jsonify(cart_data)


@cart_routes.route('/cart/<int:cart_id>', methods=['PUT'])
def update_cart(cart_id):
    item = Cart.query.get_or_404(cart_id)
    data = request.json
    item.quantity = data.get('quantity', item.quantity)
    db.session.commit()
    return jsonify({'message': 'Cart updated'})


@cart_routes.route('/cart/<int:cart_id>', methods=['DELETE'])
def delete_cart_item(cart_id):
    item = Cart.query.get_or_404(cart_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed from cart'})
