from flask import Blueprint, request, jsonify
from models import db, Register

register_routes = Blueprint('register_routes', __name__)

@register_routes.route('/register-details', methods=['POST'])
def create_register():
    data = request.json

    new_register = Register(
        login_id=data['login_id'],
        address_line1=data.get('address_line1'),
        address_line2=data.get('address_line2'),
        city=data.get('city'),
        state=data.get('state'),
        postal_code=data.get('postal_code'),
        country=data.get('country')
    )

    db.session.add(new_register)
    db.session.commit()
    return jsonify({"message": "Register details added successfully"}), 201


@register_routes.route('/register-details', methods=['GET'])
def get_all_registers():
    registers = Register.query.all()
    result = []
    for reg in registers:
        result.append({
            "register_id": reg.register_id,
            "login_id": reg.login_id,
            "address_line1": reg.address_line1,
            "address_line2": reg.address_line2,
            "city": reg.city,
            "state": reg.state,
            "postal_code": reg.postal_code,
            "country": reg.country
        })
    return jsonify(result), 200

