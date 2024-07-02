from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username
    
    @classmethod
    def create_user(cls, username, email, password):
        new_user = cls(
            username=username,
            email=email,
            password_hash=generate_password_hash(password),
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        db.session.add(new_user)
        try:
            db.session.commit()
            return new_user
        except Exception as e:
            db.session.rollback()
            raise e
    
    @classmethod
    # This method is used to authenticate a user when logging in
    def authenticate(cls, username, password):
        user = cls.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            return user

