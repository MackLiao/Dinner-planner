from flask import request, jsonify
from app import db
from models.foodModel import Food
from models.userFridgeModel import UserFridge
from datetime import datetime

def search_food():
    query = request.args.get('query', '')
    # Use the LIKE operator to search for food items that contain the query string
    # '%' is a wildcard character that matches any sequence of characters
    food_items = Food.query.filter(Food.name.like(f'%{query}%')).all()
    return jsonify([item.serialize() for item in food_items])

def add_food(user_id, food_id, quantity, best_before, weight):
    try:
        if best_before:
            best_before = datetime.strptime(best_before, '%Y-%m-%d')
    except:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD'}), 400
    new_item = UserFridge(user_id=user_id, food_id=food_id, quantity=quantity, best_before=best_before, weight=weight)
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.serialize())

def delete_food(user_id, food_id):
    item = UserFridge.query.filter_by(user_id=user_id, food_id=food_id).first()
    if item:
        db.session.delete(item)
        db.session.commit()
        return jsonify({'message': 'Item deleted successfully'})
    return jsonify({'message': 'Item not found'}), 404

def search_user_fridge(user_id):
    items = UserFridge.query.filter_by(user_id=user_id).all()
    return jsonify([item.serialize() for item in items])

def get_food_list():
    food_items = Food.query.all()
    return jsonify(food_list=[item.serialize() for item in food_items])

# Update the quantity, weight, or best before date of a fridge item
def update_food(user_id, food_id, quantity=None, weight=None, best_before=None):
    item = UserFridge.query.filter_by(user_id=user_id, food_id=food_id).first()
    try:
        if best_before:
            best_before = datetime.strptime(best_before, '%Y-%m-%d')
    except:
        return jsonify({'message': 'Invalid date format. Please use YYYY-MM-DD'}), 400
    if item:
        if quantity is not None:
            item.quantity = quantity
        if weight is not None:
            item.weight = weight
        if best_before is not None:
            item.best_before = best_before
        db.session.commit()
        return jsonify(item.serialize())
    return jsonify({'message': 'Item not found'}), 404