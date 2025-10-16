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

# ✅ CREATE USER (superadmin only, adds user under their organization)
@user_bp.route("/", methods=["POST"])
@role_required(["superadmin"])
def create_user():
    current_user_id = int(get_jwt_identity())
    current_user = User.query.get(current_user_id)

    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")  # ✅ allow password input
    role = data.get("role", "user")
    is_active = data.get("is_active", True)

    # ✅ Validate required fields
    if not name or not email or not password:
        return {"msg": "Name, email, and password are required"}, 400

    if User.query.filter_by(email=email).first():
        return {"msg": "Email already exists"}, 400

    # ✅ New users inherit Super Admin's organization
    organization = current_user.organization

    # ✅ Restrict role assignment — Super Admin can’t create another Super Admin for now
    if role not in ["user", "admin"]:
        return {"msg": "Invalid role"}, 400

    new_user = User(
        name=name,
        email=email,
        role=role,
        is_active=is_active,
        organization=organization
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    log_action(current_user_id, f"Added new user {email} (role={role}) under {organization}")

    return jsonify({
        "msg": f"User {name} added successfully under {organization}",
        "id": new_user.id,
        "name": new_user.name,
        "email": new_user.email,
        "role": new_user.role,
        "organization": new_user.organization,
        "is_active": new_user.is_active
    }), 201




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
            "ip_address": log.ip_address
        } for log in logs
    ])
