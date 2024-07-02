from flask_sqlalchemy import SQLAlchemy
from backend import app

db = SQLAlchemy(app) # Create a SQLAlchemy object with the app object

class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    carb = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Food %r>' % self.name