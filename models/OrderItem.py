from models import db

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    orderItem_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.coupon_id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    total_amt = db.Column(db.Numeric(10, 2))
