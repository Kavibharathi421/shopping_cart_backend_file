from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .Cart import Cart
from .Coupons import Coupons
from .Categories import Categories
from .Login import Login
from .OrderItem import OrderItem
from .Orders import Orders
from .ProductReviews import ProductReviews
from .Register import Register
from  .Products import Products