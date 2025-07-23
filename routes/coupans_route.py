from flask import Blueprint, request, jsonify
from models import db, Coupons
from datetime import datetime

coupon_routes = Blueprint('coupon_routes', __name__)

@coupon_routes.route('/coupons', methods=['POST'])
def create_coupon():
    data = request.json
    code = data.get('code')
    discount_percent = data.get('discount_percent')
    expiry_date = data.get('expiry_date')
    min_order_value = data.get('min_order_value')

    try:
        new_coupon = Coupons(
            code=code,
            discount_percent=discount_percent,
            expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d'),
            min_order_value=min_order_value
        )
        db.session.add(new_coupon)
        db.session.commit()
        return jsonify({'message': 'Coupon created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@coupon_routes.route('/coupons', methods=['GET'])
def get_coupons():
    coupons = Coupons.query.all()
    results = []
    for c in coupons:
        results.append({
            'coupon_id': c.coupon_id,
            'code': c.code,
            'discount_percent': str(c.discount_percent),
            'expiry_date': c.expiry_date.strftime('%Y-%m-%d'),
            'min_order_value': str(c.min_order_value)
        })
    return jsonify(results)


@coupon_routes.route('/coupons/<int:coupon_id>', methods=['GET'])
def get_coupon(coupon_id):
    coupon = Coupons.query.get_or_404(coupon_id)
    return jsonify({
        'coupon_id': coupon.coupon_id,
        'code': coupon.code,
        'discount_percent': str(coupon.discount_percent),
        'expiry_date': coupon.expiry_date.strftime('%Y-%m-%d'),
        'min_order_value': str(coupon.min_order_value)
    })




@coupon_routes.route('/coupons/<int:coupon_id>', methods=['PUT'])
def update_coupon(coupon_id):
    coupon = Coupons.query.get_or_404(coupon_id)
    data = request.json

    coupon.code = data.get('code', coupon.code)
    coupon.discount_percent = data.get('discount_percent', coupon.discount_percent)
    if data.get('expiry_date'):
        coupon.expiry_date = datetime.strptime(data['expiry_date'], '%Y-%m-%d')
    coupon.min_order_value = data.get('min_order_value', coupon.min_order_value)

    db.session.commit()
    return jsonify({'message': 'Coupon updated successfully'})

    

@coupon_routes.route('/coupons/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    coupon = Coupons.query.get_or_404(coupon_id)
    db.session.delete(coupon)
    db.session.commit()
    return jsonify({'message': 'Coupon deleted successfully'})
