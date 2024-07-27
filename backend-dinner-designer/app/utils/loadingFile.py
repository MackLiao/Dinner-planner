import sys
from pathlib import Path
import pandas as pd
import os


# Add the parent directory to sys.path to find the app module
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app import db, create_app
from models.foodModel import Food

app = create_app()

# test table initialization
# def initialize_food_table():
#     with app.app_context():
#         db.create_all() 
#         dataset = [
#             {"name": "Apple", "calories": 95, "carb": 25, "protein": 0.5, "fat": 0.3, "category": "Fruit"},
#             {"name": "Chicken Breast", "calories": 165, "carb": 0, "protein": 31, "fat": 3.6, "category": "Meat"},
#             {"name": "Banana", "calories": 35, "carb": 65, "protein": 3.5, "fat": 1.3, "category": "Fruit"},
#             {"name": "Spinach", "calories": 23, "carb": 3.6, "protein": 2.9, "fat": 0.4, "category": "Vegetable"},
#             {"name": "Salmon", "calories": 208, "carb": 0, "protein": 20, "fat": 13, "category": "Fish"},
#             {"name": "Egg", "calories": 155, "carb": 1.1, "protein": 13, "fat": 11, "category": "Dairy"},
#             {"name": "Almonds", "calories": 579, "carb": 21.6, "protein": 21.2, "fat": 49.9, "category": "Nuts"},
#             {"name": "Quinoa", "calories": 120, "carb": 21, "protein": 4.1, "fat": 1.9, "category": "Grain"}
#         ]
    
#         for item in dataset:
#             if not Food.query.filter_by(name=item["name"]).first():
#                 food_item = Food(name=item["name"], calories=item["calories"], carb=item["carb"],
#                                 protein=item["protein"], fat=item["fat"], category=item["category"])
#                 db.session.add(food_item)
#         db.session.commit()

def load_food_data(file_path):
    with app.app_context():
        db.create_all()
        clear_food_table()
        data = clean_food_data(file_path)
        for index, row in data.iterrows():
            if not Food.query.filter_by(name=row["Food"]).first():
                coef = float(row["Grams"].replace(',', '')) / 100
                food_item = Food(
                    name=row["Food"], 
                    calories=int(row["Calories"] / coef), 
                    carb=int(row["Carbs"] / coef),
                    protein=int(row["Protein"] / coef), 
                    fat=int(row["Fat"] / coef), 
                    category=row["Category"]
                )
                db.session.add(food_item)
        db.session.commit()
    print("Data loaded successfully")

def clean_food_data(file_path):
    try:
        data = pd.read_csv(file_path)
        data = data.dropna(axis=0)

        # Replace any non-numeric characters with '0' and convert to float
        data['Calories'] = data['Calories'].str.replace(',', '').replace(r'\D', '0', regex=True).astype(float)
        data['Carbs'] = data['Carbs'].str.replace(r'\D', '0', regex=True).astype(float)
        data['Protein'] = data['Protein'].str.replace(r'\D', '0', regex=True).astype(float)
        data['Fat'] = data['Fat'].str.replace(r'\D', '0', regex=True).astype(float)
        
        return data
    except Exception as e:
        print(e)
        return None

# Clear the previous data in the food table
def clear_food_table():
    with app.app_context():
        db.session.query(Food).delete()
        db.session.commit()


if __name__ == "__main__":
    load_food_data(os.getenv("FOOD_DATA_PATH"))