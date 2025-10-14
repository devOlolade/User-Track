from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, AuditLog
from app.utils.auth import role_required
from app.utils.audit import log_action
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
    
    log_action(user_id, "Viewed own profile")

    return jsonify({
        "id": user.id,
        "name": user.name,
        "email": user.email
    }), 200

#CREATE a new user (admin or superadmin only)
@user_bp.route("/", methods=["POST"])
@role_required(["admin", "superadmin"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    role = data.get("role", "user")
    is_active = data.get("is_active", True)

    if not name or not email:
        return {"msg": "Name and email are required"}, 400
    
    if role not in ["user", "admin", "superadmin"]:
        return {"msg": "Invalid role"}, 400

    new_user = User(name=name, email=email, role=role, is_active=is_active)
    db.session.add(new_user)
    db.session.commit()

    current_user_id = int(get_jwt_identity())
    log_action(current_user_id, f"Created user {new_user.id} ({new_user.email}, role={new_user.role})")

    return jsonify({
        "msg": "User created successfully",
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
        "is_active": new_user.is_active
    }), 201

#list all users
@user_bp.route("/", methods=["GET"])
@role_required(["admin", "superadmin"])
def list_users():
    current_user_id = int(get_jwt_identity())
    users = User.query.all()

    log_action(current_user_id, "Viewed all users")
    return jsonify([
        {"id": u.id, "name": u.name, "email": u.email, "role": u.role, "is_active": u.is_active}
        for u in users
    ]), 200

#GET a specific user by ID
@user_bp.route("/<int:user_id>", methods=["GET"])
@role_required(["admin", "superadmin"])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404
    
    current_user_id = int(get_jwt_identity())
    log_action(current_user_id, f"Viewed user {user.id}")

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

    current_user_id = int(get_jwt_identity())
    log_action(current_user_id, f"Updated user {user.id} (role={user.role}, is_active={user.is_active})")

    return jsonify ({
        "msg": "User updated successfully",
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active
    }), 200

#  TOGGLE USER STATUS
@user_bp.route("/<int:user_id>/toggle-status", methods=["PATCH"])
@role_required(["admin", "superadmin"])
def toggle_user_status(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404

    user.is_active = not user.is_active
    db.session.commit()

    current_user_id = int(get_jwt_identity())
    status = "activated" if user.is_active else "deactivated"
    log_action(current_user_id, f"Toggled user {user.id} status → {status}")

    return jsonify({
        "msg": f"User {status} successfully",
        "id": user.id,
        "is_active": user.is_active
    }), 200


# ✅ DELETE USER
@user_bp.route("/<int:user_id>", methods=["DELETE"])
@role_required(["admin", "superadmin"])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return {"msg": "User not found"}, 404

    db.session.delete(user)
    db.session.commit()

    current_user_id = int(get_jwt_identity())
    log_action(current_user_id, f"Deleted user {user_id}")

    return {"msg": "User deleted successfully"}, 200

#VIEW AUDIT LOGS (admin or superadmin only)
@user_bp.route('/audit-logs', methods=['GET'])
@jwt_required()
def get_audit_logs():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user or user.role not in ["admin", "superadmin"]:
        return jsonify({"error": "Unauthorized"}), 403

    logs = AuditLog.query.order_by(AuditLog.timestamp.desc()).all()

    log_action(user_id, "Viewed audit logs")
    return jsonify([
        {
            "id": log.id,
            "user_id": log.user_id,
            'actor': log.actor,
            "action": log.action,
            "timestamp": log.timestamp.isoformat(),
            "ip": log.ip_address
        } for log in logs
    ])
