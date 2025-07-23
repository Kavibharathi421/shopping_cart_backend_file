from flask import Blueprint, request, jsonify
from models import db, Orders
from datetime import datetime

order_routes = Blueprint('order_routes', __name__)

# Create a new order
@order_routes.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    login_id = data.get('login_id')
    register_id = data.get('register_id')
    payment_method = data.get('payment_method')

    order = Orders(login_id=login_id, register_id=register_id, payment_method=payment_method)
    db.session.add(order)
    db.session.commit()

    return jsonify({'message': 'Order created successfully', 'order_id': order.order_id})

@order_routes.route('/orders', methods=['GET'])
def get_orders():
    orders = Orders.query.all()
    return jsonify([
        {
            'order_id': order.order_id,
            'login_id': order.login_id,
            'register_id': order.register_id,
            'payment_method': order.payment_method
        }
        for order in orders
    ])

@order_routes.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Orders.query.get_or_404(order_id)
    return jsonify({
        'order_id': order.order_id,
        'login_id': order.login_id,
        'register_id': order.register_id,
        'payment_method': order.payment_method
    })

@order_routes.route('/orders/<int:order_id>' ,methods=['PUT'])
def update_order(order_id):
    orders=Orders.query.get_or_404(order_id)
    data=request.json
    for fields in data:
        setattr(orders,fields,data[fields])
        db.session.commit()
    return jsonify("orders updated successfully")

@order_routes.route('/orders/<int:order_id>' ,methods=['DELETE'])
def delete_order(order_id):
    orders=Orders.query.get_or_404(order_id)
    db.session.delete(orders)
    db.session.commit()
    return jsonify("order deleted successfully")
