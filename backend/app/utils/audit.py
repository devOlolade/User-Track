from flask import request
from app import db
from app.models import AuditLog, User
from flask_jwt_extended import get_jwt_identity

def log_action(user_id, action):
    """Log user actions for audit trail"""
    user = User.query.get(user_id)
    actor_name = user.email if user else f"User {user_id}"

    log = AuditLog(
        user_id=user_id,
        actor=actor_name,
        action=action,
        ip_address=request.remote_addr
    )
    db.session.add(log)
    db.session.commit()
