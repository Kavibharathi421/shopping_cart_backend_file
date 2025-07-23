from models import db

class Categories(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

    products = db.relationship('Products', backref='category', cascade="all, delete-orphan")
