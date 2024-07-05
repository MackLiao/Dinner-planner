from flask import Blueprint, request
from services.foodService import search_food, add_food, delete_food, search_user_fridge, update_food

food_routes = Blueprint('food_routes', __name__)

@food_routes.route('/search_food', methods=['GET'])
def handle_search_food():
    return search_food()

@food_routes.route('/add_food', methods=['POST'])
def handle_add_food():
    data = request.get_json()
    user_id = data.get('user_id')
    food_id = data.get('food_id')
    quantity = data.get('quantity')
    best_before = data.get('best_before')
    weight = data.get('weight')
    return add_food(user_id, food_id, quantity, best_before, weight)

@food_routes.route('/delete_food/<int:user_id>/<int:food_id>', methods=['DELETE'])
def handle_delete_food(user_id, food_id):
    return delete_food(user_id, food_id)

@food_routes.route('/search_user_fridge/<int:user_id>', methods=['GET'])
def handle_search_user_fridge(user_id):
    return search_user_fridge(user_id)

@food_routes.route('/update_food', methods=['PUT'])
def handle_update_food():
    data = request.get_json()
    user_id = data.get('user_id')
    food_id = data.get('food_id')
    quantity = data.get('quantity')
    weight = data.get('weight')
    best_before = data.get('best_before')
    return update_food(user_id, food_id, quantity, weight, best_before)