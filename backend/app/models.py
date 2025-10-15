from . import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(db.Model):
    __tablename__ = "users" 

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="user")  # 👈 new field
    is_active = db.Column(db.Boolean, default=True) 

   

    def __repr__(self):
        return f"<User {self.email}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password,  method="pbkdf2:sha256")

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    

class AuditLog(db.Model):
    __tablename__ = "audit_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    actor = db.Column(db.String(120)) 
    action = db.Column(db.String(255), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)

    user = db.relationship("User", backref="audit_logs")


    def __repr__(self):
        return f"<AuditLog {self.action} by User {self.user_id} at {self.timestamp} from {self.ip_address}>"