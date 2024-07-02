from flask import Blueprint
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
from models.userModel import User
from services.authService import authenticate, create_user, delete_user

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    user = authenticate(username, password)

    if user:
        access_token = create_access_token(identity=username, expires_delta=timedelta(days=1))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401
    
@auth_blueprint.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200

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