from flask import Blueprint, request
from services.foodService import get_food_list, search_food, add_food, delete_food, search_user_fridge, update_food
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

food_routes = Blueprint('food_routes', __name__)

@food_routes.route('/search_food', methods=['GET'])
def handle_search_food():
    return search_food()

@food_routes.route('/get_food_list', methods=['GET'])
def handle_get_food_list():
    return get_food_list()

@food_routes.route('/add_food', methods=['POST'])
@jwt_required()
def handle_add_food():
    user_id = get_jwt_identity()
    data = request.get_json()
    food_id = data.get('food_id')
    quantity = data.get('quantity')
    best_before = data.get('best_before')
    weight = data.get('weight')
    return add_food(user_id, food_id, quantity, best_before, weight)

@food_routes.route('/delete_food', methods=['DELETE'])
@jwt_required()
def handle_delete_food():
    data = request.get_json()
    food_id = data.get('food_id')
    user_id = get_jwt_identity()
    return delete_food(user_id, food_id)

@food_routes.route('/search_user_fridge', methods=['GET'])
@jwt_required()
def handle_search_user_fridge():
    user_id = get_jwt_identity()
    return search_user_fridge(user_id)

@food_routes.route('/update_food', methods=['PUT'])
@jwt_required()
def handle_update_food():
    data = request.get_json()
    user_id = get_jwt_identity()
    food_id = data.get('food_id')
    quantity = data.get('quantity')
    weight = data.get('weight')
    best_before = data.get('best_before')
    return update_food(user_id, food_id, quantity, weight, best_before)