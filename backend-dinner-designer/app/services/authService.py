from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from models.userModel import User, db


def create_user(username, email, password):
    new_user = User(
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

# This method is used to authenticate a user when logging in
def authenticate(username, password):
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password_hash, password):
        return user
    

def delete_user(id):
    user = User.query.filter_by(id=id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return user
    else:
        return None

