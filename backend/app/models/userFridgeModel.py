from flask_sqlalchemy import SQLAlchemy
from app import db

class UserFridge(db.Model):
    __tablename__ = 'user_fridges'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    added_on = db.Column(db.DateTime, default=db.func.current_timestamp())
    best_before = db.Column(db.DateTime, nullable=True)
    weight = db.Column(db.Integer, nullable=True)

    # Define relationships
    # This line creates a relationship between the UserFridge model and the User model. 
    # It means each UserFridge instance will have a user attribute through which you can access the associated User object.
    # The backref argument creates a virtual column fridge_items on the User model, allowing you to access a list of UserFridge instances related to a User.
    # For example, some_user.fridge_items would give you all fridge items belonging to some_user.
    user = db.relationship('User', backref=db.backref('fridge_items', lazy=True)) 
    food = db.relationship('Food', backref=db.backref('users', lazy=True))

    def __repr__(self):
        return f'<UserFridge {self.user_id} {self.food_id}>'