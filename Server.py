from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Login(db.Model):
    __tablename__ = 'login'
    login_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20))
    role = db.Column(db.Enum('admin', 'customer', name='user_roles'), default='customer')

    register = db.relationship('Register', backref='login', uselist=False)
    cart_items = db.relationship('Cart', backref='login', cascade="all, delete-orphan")
    orders = db.relationship('Orders', backref='login', cascade="all, delete-orphan")
    reviews = db.relationship('ProductReviews', backref='login', cascade="all, delete-orphan")


class Register(db.Model):
    __tablename__ = 'register'
    register_id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'))
    address_line1 = db.Column(db.String(255))
    address_line2 = db.Column(db.String(255))
    city = db.Column(db.String(100))
    state = db.Column(db.String(100))
    postal_code = db.Column(db.String(20))
    country = db.Column(db.String(100))

    orders = db.relationship('Orders', backref='register', cascade="all, delete-orphan")


class Categories(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    products = db.relationship('Products', backref='category', cascade="all, delete-orphan")


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


class Coupons(db.Model):
    __tablename__ = 'coupons'
    coupon_id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), nullable=False)
    discount_percent = db.Column(db.Numeric(5, 2))
    expiry_date = db.Column(db.Date)
    min_order_value = db.Column(db.Numeric(10, 2))

    order_items = db.relationship('OrderItem', backref='coupon', cascade="all, delete-orphan")


class Cart(db.Model):
    __tablename__ = 'cart'
    cart_id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer)

    order_items = db.relationship('OrderItem', backref='cart', cascade="all, delete-orphan")


class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'))
    register_id = db.Column(db.Integer, db.ForeignKey('register.register_id'))
    payment_method = db.Column(db.String(50))

    order_items = db.relationship('OrderItem', backref='order', cascade="all, delete-orphan")


class OrderItem(db.Model):
    __tablename__ = 'order_item'
    orderItem_id = db.Column(db.Integer, primary_key=True)
    cart_id = db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
    coupon_id = db.Column(db.Integer, db.ForeignKey('coupons.coupon_id'), nullable=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    total_amt = db.Column(db.Numeric(10, 2))
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))


class ProductReviews(db.Model):
    __tablename__ = 'product_reviews'
    review_id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    rating = db.Column(db.Integer)
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
