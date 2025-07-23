from models import db


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
