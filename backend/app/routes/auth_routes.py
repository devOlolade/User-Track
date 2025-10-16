from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_jwt_extended import create_access_token, decode_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from flask_mail import Message
from app import mail
from datetime import timedelta
from app.utils.audit import log_action

auth_bp = Blueprint("auth", __name__)

# ✅ SUPER ADMIN ONLY REGISTRATION
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")
    organization = data.get("organization")

     # Basic validation
    if not name or not email or not password or not organization:
        return jsonify({"message": "All fields are required"}), 400

    # Check if user email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    # Check if the organization already has a superadmin
    existing_org = User.query.filter_by(organization=organization).first()

    if existing_org:
        # Org already exists → reject registration
        return jsonify({
            "message": "An account for this organization already exists. Please contact your Super Admin."
        }), 400

    # ✅ Create first user as Super Admin for this organization
    new_user = User(
        name=name,
        email=email,
        organization=organization,
        role="superadmin"
    )
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful! You are the Super Admin for this organization.",
        "role": new_user.role
    }), 201
   
# ✅ LOGIN ENDPOINT
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return {"msg": "Invalid email or password"}, 401

    access_token = create_access_token(identity=user.id)
    log_action(user.id, "User logged in")

    return jsonify({
        "access_token": access_token,
        "role": user.role,
        "name": user.name
    }), 200


# ✅ PASSWORD MANAGEMENT ENDPOINTS (unchanged)
@auth_bp.route('/change-password', methods=['PUT'])
@jwt_required()
def change_password():
    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return jsonify({"msg": "Both old and new passwords are required"}), 400

    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"msg": "User not found"}), 404

    if not user.check_password(old_password):
        return jsonify({"msg": "Old password is incorrect"}), 400

    user.set_password(new_password)
    db.session.commit()

    log_action(user.id, "Changed password")
    return jsonify({"msg": "Password updated successfully!"}), 200


@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"msg": "Email is required"}), 400
    
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"msg": "User with this email does not exist"}), 404
    
    reset_token = create_access_token(identity=user.id, expires_delta=timedelta(minutes=15))
    reset_link = f"http://127.0.0.1:5000/auth/reset-password/{reset_token}"

    msg = Message("Password Reset Request",
                  sender="olukayodelolade@gmail.com",
                  recipients=[email])
    msg.body = f"Click the link to reset your password: {reset_link}"
    mail.send(msg)

    log_action(user.id, "Requested password reset")
    return jsonify({"msg": "Password reset link sent to email!"}), 200


@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token["sub"]
    except Exception:
        return jsonify({"msg": "Invalid or expired token"}), 400

    data = request.get_json()
    new_password = data.get("new_password")

    if not new_password:
        return jsonify({"msg": "New password is required"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg": "User not found"}), 404

    user.password = generate_password_hash(new_password)
    db.session.commit()

    log_action(user.id, "Password reset successful")
    return jsonify({"msg": "Password reset successful!"}), 200
