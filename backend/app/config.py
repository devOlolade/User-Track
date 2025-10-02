import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "supersecretkey"
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "postgresql://usertrack_user:usertrack_pass@localhost:5432/UserTrack"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "jwt-secret-key"

    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = "olukayodelolade@gmail.com"  # replace with your Gmail
    MAIL_PASSWORD = "gmdh ezlz xqtz wqwqd"    # use Google App Password
    MAIL_DEFAULT_SENDER = "olukayodelolade@gmail.com"