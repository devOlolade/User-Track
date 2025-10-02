from . import db, bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

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