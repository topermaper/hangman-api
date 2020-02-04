from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# Start Flask app
app = Flask(__name__)
app.config.from_object('configuration.DevelopmentConfig')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Import JWT
jwt = JWTManager(app)

# import API
from app.api.api import api, Users, Games, Token, Login
api.prefix = app.config["BASE_API_URL"]
api.add_resource(Users, "/users", "/users/<int:id>")
api.add_resource(Games, "/games", "/games/<int:id>")
api.add_resource(Token, "/token")
api.add_resource(Login, '/login')
api.init_app(app)

# Build DB
db.create_all()