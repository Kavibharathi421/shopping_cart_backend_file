from models import db

class Orders(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    login_id = db.Column(db.Integer, db.ForeignKey('login.login_id'))
    register_id = db.Column(db.Integer, db.ForeignKey('register.register_id'))
    payment_method = db.Column(db.String(50))

