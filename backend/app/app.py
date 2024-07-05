from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') # Secret key for JWT
db = SQLAlchemy(app)
jwt = JWTManager(app)

from routes.authRoutes import auth_blueprint
from routes.foodRoutes import food_routes

app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(food_routes, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)

@app.cli.command("create-db")
def create_db():
    """Create the database and tables."""
    db.create_all()
    print("Database and tables created.")