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

#from app.models.user import User
#from app.models.game import Game

# import API
from app.api.api import api, Token, Login #, Users, Games
api.prefix = app.config["BASE_API_URL"]
#api.add_resource(Users, "/user", "/users/<int:id>")
#api.add_resource(Games, "/game", "/games/<int:id>")
api.add_resource(Token, "/token")
api.add_resource(Login, '/login')
api.init_app(app)

# Build DB
db.create_all()