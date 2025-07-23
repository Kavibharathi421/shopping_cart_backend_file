from models import db
from datetime import datetime

class ProductReviews(db.Model):
    __tablename__ = 'product_reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
