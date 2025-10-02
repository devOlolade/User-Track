from flask import Blueprint, request, jsonify
from app.models import db, User
from flask_jwt_extended import create_access_token, decode_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Message, Mail
from app import mail
from datetime import timedelta
import secrets


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    new_user = User(name=name, email=email)
    new_user.set_password(password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):  # ✅ check hash
        return {"msg": "Invalid email or password"}, 401
    access_token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": access_token}), 200
from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, db

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

    return jsonify({"msg": "Password reset link sent to email!"}), 200

@auth_bp.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    try:
        decoded_token = decode_token(token)
        user_id = decoded_token["sub"]
    except Exception as e:
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

    return jsonify({"msg": "Password reset successful!"}), 200

