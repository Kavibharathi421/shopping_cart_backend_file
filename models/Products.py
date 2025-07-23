from models import db

class Products(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    stock_qty = db.Column(db.Integer)
    image_url = db.Column(db.String(255))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))

    cart_items = db.relationship('Cart', backref='product', cascade="all, delete-orphan")
    order_items = db.relationship('OrderItem', backref='product', cascade="all, delete-orphan")
    reviews = db.relationship('ProductReviews', backref='product', cascade="all, delete-orphan")
