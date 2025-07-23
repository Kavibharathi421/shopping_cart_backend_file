from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Login

login_routes = Blueprint('login_routes', __name__)

@login_routes.route('/login', methods=['POST'])
def register_user():
    data = request.json
    hashed_password = generate_password_hash(data['password'])

    new_user = Login(
        name=data.get('name'),
        email=data['email'],
        password=hashed_password,
        phone_number=data.get('phone_number'),
        role=data.get('role', 'customer')
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User registered successfully"}), 201


# 📃 Get All Users
@login_routes.route('/users', methods=['GET'])
def get_all_users():
    users = Login.query.all()
    user_list = []
    for user in users:
        user_list.append({
            "login_id": user.login_id,
            "name": user.name,
            "email": user.email,
            "phone_number": user.phone_number,
            "role": user.role
        })
    return jsonify(user_list), 200


# 📄 Get Single User
@login_routes.route('/users/<int:login_id>', methods=['GET'])
def get_user(login_id):
    user = Login.query.get_or_404(login_id)
    return jsonify({
        "login_id": user.login_id,
        "name": user.name,
        "email": user.email,
        "phone_number": user.phone_number,
        "role": user.role
    })


@login_routes.route('/users/<int:login_id>', methods=['PUT'])
def update_user(login_id):
    user = Login.query.get_or_404(login_id)
    data = request.json
    for field in data:
        setattr(user,field,data[field])
    if 'password' in data:
        user.password = generate_password_hash(data['password'])

    db.session.commit()
    return jsonify({"message": "User updated successfully"})


@login_routes.route('/users/<int:login_id>', methods=['DELETE'])
def delete_user(login_id):
    user = Login.query.get_or_404(login_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
