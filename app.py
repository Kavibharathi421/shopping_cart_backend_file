from flask import Flask
from models import db, Login, OrderItem, Orders, ProductReviews, Products, Register, Cart, Categories, Coupons
from routes._init_ import register_route
from flask_cors import CORS

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Kavi%40123@localhost:3306/shop'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
register_route(app)
CORS(app)

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
