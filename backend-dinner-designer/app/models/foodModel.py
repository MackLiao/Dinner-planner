from flask_sqlalchemy import SQLAlchemy
from app import db

class Food(db.Model):
    __tablename__ = 'foods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    carb = db.Column(db.Integer, nullable=False)
    protein = db.Column(db.Integer, nullable=False)
    fat = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'calories': self.calories,
            'carb': self.carb,
            'protein': self.protein,
            'fat': self.fat,
            'category': self.category
        }

    def __repr__(self):
        return '<Food %r>' % self.name