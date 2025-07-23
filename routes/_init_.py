from .login_route import login_routes
from .cart_route import cart_routes
from .category_route import category_routes
from .productesreview_route import product_reviews_bp
from .coupans_route import coupon_routes
from .order_route import order_routes
from .register_route import register_routes
from .orderitem_route import orderitem_route
from .products_route import product_routes

def register_route(app):
    app.register_blueprint(order_routes)
    app.register_blueprint(orderitem_route)
    app.register_blueprint(product_reviews_bp)
    app.register_blueprint(category_routes)
    app.register_blueprint(cart_routes)
    app.register_blueprint(coupon_routes)
    app.register_blueprint(login_routes)
    app.register_blueprint(register_routes)
    app.register_blueprint(product_routes)

