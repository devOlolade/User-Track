from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User
from app.utils.auth import role_required
from app import db

user_bp = Blueprint("users", __name__)

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    """Return the current user's profile"""
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    }), 200

@user_bp.route("/", methods=["GET"])
@role_required(["admin", "superadmin"])
def list_users():
    users = User.query.all()
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email, "role": u.role, "is_active": u.is_active}
        for u in users
    ]), 200


@user_bp.route("/<int:user_id>", methods=["GET"])
@role_required(["admin", "superadmin"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }, 200

@user_bp.route("/<int:user_id>", methods=["PUT"])
@role_required(["admin", "superadmin"])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404

    data = request.get_json()
    role = data.get("role")
    is_active = data.get("is_active")

    # Only allow valid roles
    if role and role not in ["user", "admin", "superadmin"]:
        return {"msg": "Invalid role"}, 400

    if role:
        user.role = role
    if is_active is not None:  # could be True or False
        user.is_active = is_active

    db.session.commit()

    return jsonify ({
        "msg": "User updated successfully",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }), 200
