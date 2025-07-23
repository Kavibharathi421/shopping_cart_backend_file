from models import db


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
