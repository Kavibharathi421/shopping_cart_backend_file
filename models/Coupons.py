from models import db


class Coupons(db.Model):
    __tablename__ = 'coupons'
    coupon_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    discount_percent = db.Column(db.Numeric(5, 2))
    expiry_date = db.Column(db.Date)
    min_order_value = db.Column(db.Numeric(10, 2))

    order_items = db.relationship('OrderItem', backref='coupon', cascade="all, delete-orphan")
