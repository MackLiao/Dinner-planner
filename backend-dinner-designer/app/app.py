from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') # Secret key for JWT
# This line already creates the SQLAlchemy object with the app object
# No need to initialize it again.
db = SQLAlchemy(app) 
jwt = JWTManager(app)

# Import routes here after db is defined to avoid circular imports
# Since routes import db from services, and services import db from app
from routes.authRoutes import auth_blueprint
from routes.foodRoutes import food_routes

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(food_routes, url_prefix='/')

def create_app():
    app = Flask(__name__)
    
    # Configure your Flask app here, e.g., database URI
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    
    db.init_app(app)
    
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(food_routes, url_prefix='/')

    return app

if __name__ == '__main__':
    app.run(debug=True)

@app.cli.command("create-db")
def create_db():
    """Create the database and tables."""
    db.create_all()
    print("Database and tables created.")