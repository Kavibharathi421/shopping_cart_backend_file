# routes/orderitem_route.py
from flask import Blueprint, request, jsonify
from models import db, Cart, OrderItem, Coupons, Products
from datetime import datetime

orderitem_route = Blueprint('orderitem_route', __name__)

@orderitem_route.route('/add-order-items', methods=['POST'])
def add_order_items():
    data = request.json
    login_id = data.get('login_id')
    coupon_code = data.get('coupon_code')


    coupon = None
    discount_percent = 0

    if coupon_code:
        coupon = Coupons.query.filter_by(code=coupon_code,discount_percent=discount_percent).first()
        if not coupon:
            return jsonify({'error': 'Invalid coupon'}), 400
        if datetime.utcnow().date() > coupon.expiry_date:
            return jsonify({'error': 'Coupon expired'}), 400
        discount_percent = float(coupon.discount_percent)

    # Get cart items for the user
    cart_items = Cart.query.filter_by(login_id=login_id).all()
    if not cart_items:
        return jsonify({'error': 'No items in cart'}), 400

    for item in cart_items:
        price = float(item.product.price)
        qty = item.quantity
        total = price * qty
        if discount_percent > 0:
            total -= (total * discount_percent / 100)

        order_item = OrderItem(
            cart_id=item.cart_id,
            product_id=item.product_id,
            coupon_id=coupon.coupon_id if coupon else None,
            total_amt=total
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'message': 'Order items added and cart cleared'})


@orderitem_route.route('/order-items', methods=['GET'])
def get_order_items():
    order_items = OrderItem.query.all()
    result = []

    for item in order_items:
        result.append({
            'order_item_id': item.orderItem_id,
            'product_id': item.product_id,
            'product_name': item.product.name if item.product else None,
            'quantity': item.cart.quantity if item.cart else None,
            'discount_percentage':item.coupon.discount_percent if item.coupon else None,
            'total_amount': float(item.total_amt),
            'coupon_applied': item.coupon.code if item.coupon else None,
        })
    return jsonify(result)

@orderitem_route.route('/order-items/<int:order_item_id>',methods=['DELETE'])
def delete_orderitem(order_item_id):
    order_items=OrderItem.query.get_or_404(order_item_id)
    db.session.delete(order_items)
    db.session.commit()
    return jsonify("orderitem deleted successfully")
