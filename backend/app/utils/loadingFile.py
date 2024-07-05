import sys
from pathlib import Path

# Add the parent directory to sys.path to find the app module
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import db, create_app
from models.foodModel import Food

app = create_app()

def initialize_food_table():
    with app.app_context():
        db.create_all() 
        dataset = [
            {"name": "Apple", "calories": 95, "carb": 25, "protein": 0.5, "fat": 0.3, "category": "Fruit"},
            {"name": "Chicken Breast", "calories": 165, "carb": 0, "protein": 31, "fat": 3.6, "category": "Meat"},
            {"name": "Banana", "calories": 35, "carb": 65, "protein": 3.5, "fat": 1.3, "category": "Fruit"},
            {"name": "Spinach", "calories": 23, "carb": 3.6, "protein": 2.9, "fat": 0.4, "category": "Vegetable"},
            {"name": "Salmon", "calories": 208, "carb": 0, "protein": 20, "fat": 13, "category": "Fish"},
            {"name": "Egg", "calories": 155, "carb": 1.1, "protein": 13, "fat": 11, "category": "Dairy"},
            {"name": "Almonds", "calories": 579, "carb": 21.6, "protein": 21.2, "fat": 49.9, "category": "Nuts"},
            {"name": "Quinoa", "calories": 120, "carb": 21, "protein": 4.1, "fat": 1.9, "category": "Grain"}
        ]
    
        for item in dataset:
            if not Food.query.filter_by(name=item["name"]).first():
                food_item = Food(name=item["name"], calories=item["calories"], carb=item["carb"],
                                protein=item["protein"], fat=item["fat"], category=item["category"])
                db.session.add(food_item)
        db.session.commit()


if __name__ == "__main__":
    initialize_food_table()