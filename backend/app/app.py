from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta
import os
from dotenv import load_dotenv
from models.userModel import User, db
from routes.authRoutes import auth_blueprint

load_dotenv() # Load environment variables from .env file

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY') # Secret key for JWT
db.init_app(app)
jwt = JWTManager(app)

app.register_blueprint(auth_blueprint, url_prefix='/auth')

if __name__ == '__main__':
    app.run(debug=True)

@app.cli.command("create-db")
def create_db():
    """Create the database and tables."""
    db.create_all()
    print("Database and tables created.")