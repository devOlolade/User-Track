from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from flask import jsonify
from app.models import User

def role_required(required_roles):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            user_id = int(get_jwt_identity())
            user = User.query.get(user_id)

            if user and user.role in required_roles:
                return fn(*args, **kwargs)
            else:
                return jsonify({"msg": "Access forbidden: insufficient role"}), 403
        return decorator
    return wrapper
