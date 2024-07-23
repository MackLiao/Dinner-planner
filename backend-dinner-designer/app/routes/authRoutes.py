from flask import Blueprint
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models.userModel import User
from models.foodModel import Food
from models.userFridgeModel import UserFridge
from services.authService import authenticate, create_user, delete_user
import logging


auth_blueprint = Blueprint('auth', __name__)
logging.basicConfig(level=logging.DEBUG)


@auth_blueprint.route('/login', methods=['POST'])
def login():
    email = request.json.get('email', None)
    password = request.json.get('password', None)
    rememberMe = request.json.get('rememberMe', False)
    logging.debug(f"{email}, {password}")
    
    user = authenticate(email, password)

    if user:
        access_token = create_access_token(identity=email, expires_delta=timedelta(days=7) if rememberMe else timedelta(hours=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@auth_blueprint.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user_id = get_jwt_identity()
    user_items = UserFridge.query.filter_by(user_id=user_id).all()

    # Initialize an empty list to hold the combined data
    combined_item_list = []

    for item in user_items:
        # Query the foodModel table for nutritional data using item.food_id
        food_info = Food.query.filter_by(id=item.food_id).first()

        # Combine the data from user_items and foodModel table
        if food_info:
            combined_item = {
                'food_id': item.food_id,
                'quantity': item.quantity,
                'best_before': item.best_before,
                'weight': item.weight,
                'nutritional_data': {
                    'calories': food_info.calories,
                    'protein': food_info.protein,
                    'carb': food_info.carb,
                    'fat': food_info.fat
                }
            }
            combined_item_list.append(combined_item)
            
    combined_item_list = sorted(combined_item_list, key=lambda x: x['best_before'])
    return jsonify(combined_item_list=combined_item_list), 200

@auth_blueprint.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    if not username or not email or not password:
        return jsonify({'error': 'Missing data'}), 400

    # Check if the user already exists
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({'error': 'User already exists'}), 400

    try:
        new_user = create_user(username, email, password)
        return jsonify({'message': 'User created successfully', 'user': str(new_user)}), 201
    except Exception as e:
        return jsonify({'error': 'Failed to create user', 'message': str(e)}), 500
    
# @auth_blueprint.route('/logout', methods=['POST'])
# def logout():
