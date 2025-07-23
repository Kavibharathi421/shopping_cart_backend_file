from flask import Blueprint, request, jsonify
from models import db, ProductReviews, Products, Login
from datetime import datetime

product_reviews_bp = Blueprint('product_reviews_bp', __name__)

# Create a new review
@product_reviews_bp.route('/reviews', methods=['POST'])
def add_review():
    data = request.json
    try:
        review = ProductReviews(
            login_id=data['login_id'],
            product_id=data['product_id'],
            rating=data['rating'],
            comment=data.get('comment', ''),
            created_at=datetime.utcnow()
        )
        db.session.add(review)
        db.session.commit()
        return jsonify({"message": "Review added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Get all reviews
@product_reviews_bp.route('/reviews', methods=['GET'])
def get_all_reviews():
    reviews = ProductReviews.query.all()
    review_list = []
    for review in reviews:
        review_list.append({
            "review_id": review.review_id,
            "login_id": review.login_id,
            "product_id": review.product_id,
            "rating": review.rating,
            "comment": review.comment,
            "created_at": review.created_at
        })
    return jsonify(review_list), 200

# Get reviews by product ID
@product_reviews_bp.route('/reviews/product/<int:product_id>', methods=['GET'])
def get_reviews_by_product(product_id):
    reviews = ProductReviews.query.filter_by(product_id=product_id).all()
    review_list = [{
        "review_id": r.review_id,
        "login_id": r.login_id,
        "rating": r.rating,
        "comment": r.comment,
        "created_at": r.created_at
    } for r in reviews]
    return jsonify(review_list), 200

# Update a review
@product_reviews_bp.route('/reviews/<int:review_id>', methods=['PUT'])
def update_review(review_id):
    data = request.json
    review = ProductReviews.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    for field in data:
        setattr(review,field,data[field])
    db.session.commit()
    return jsonify({"message": "Review updated"}), 200

# Delete a review
@product_reviews_bp.route('/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    review = ProductReviews.query.get(review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200
