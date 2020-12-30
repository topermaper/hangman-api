import json

from flask import request, jsonify, abort, make_response
from flask_restful import Api, Resource
from flask_restless import APIManager, ProcessingException

from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, get_jwt_identity

from app import app, db
from app.models.user import User
from app.models.game import Game
from app.models.hangman import Hangman

apimanager = APIManager(app, flask_sqlalchemy_db=db)


# Need the preprocessor to protect the endpoint with jwt
@jwt_required
def user_get_preprocessor(instance_id=None, **kw):
    pass


# Need the preprocessor to protect the endpoint with jwt
@jwt_required
def user_get_many_preprocessor(search_params=None, **kw):
    pass


# We don't need @jwt_required to create a user, everyone is allowed
def user_post_preprocessor(data=None, **kw):
    user = User.query.filter_by(email = data['email']).first()
    # this user does not exist
    if user is not None:
        raise ProcessingException(description = 'Email address already in use', code=422)

    data['password'] = generate_password_hash(data.get('password'), method='sha256')


# Need the preprocessor to protect the endpoint with jwt
@jwt_required
def game_get_preprocessor(instance_id=None, **kw):
    pass


# Need the preprocessor to protect the endpoint with jwt
@jwt_required
def game_get_many_preprocessor(search_params=None, **kw):
    pass


@jwt_required
def game_post_preprocessor(data=None, **kw):
    if data['user_id'] != get_jwt_identity():
        raise ProcessingException(description="You don't have permission to create game for user {}".format(data['user_id']),
                                  code=403)


@jwt_required
def game_patch_single_preprocessor(instance_id=None, data=None, **kw):
    hangman = Hangman.query.get(instance_id)

    if hangman == None:
        raise ProcessingException(description="Game {} does not exist".format(instance_id),
                                  code=404)

    if hangman.user_id != get_jwt_identity():
        raise ProcessingException(description="User doesn't own game {}".format(instance_id),
                                  code=403)

    if hangman.status != 'ACTIVE':
        raise ProcessingException(description="Game {} is not playable".format(instance_id),
                                  code=422)

    try:
        hangman.set_user_guess(data['user_guess'])
    except Exception as e:
        raise ProcessingException(description=str(e), code=422)
   
    # Filter data dictionary
    accepted_keys = ['user_guess']
    # Can not iterate and delete dict keys since data.keys() returns iterable so we convert to list
    for key in list(data.keys()):
        if key not in accepted_keys:
            del data[key]


apimanager.create_api(
    User,
    url_prefix      = app.config['BASE_API_URL'],
    collection_name = 'user',
    methods         = ['GET','POST'],
    exclude_columns = ['password'],
    preprocessors   = {
        'POST'       : [user_post_preprocessor],
        'GET_SINGLE' : [user_get_preprocessor],
        'GET_MANY'   : [user_get_many_preprocessor]
    }
)

apimanager.create_api(
    Game,
    url_prefix      = app.config['BASE_API_URL'],
    collection_name = 'game',
    methods         = ['GET', 'POST', 'PATCH'],
    exclude_columns = ['user_id','user.password'],
    preprocessors   = {
        'POST'         : [game_post_preprocessor],
        'GET_SINGLE'   : [game_get_preprocessor],
        'GET_MANY'     : [game_get_many_preprocessor],
        'PATCH_SINGLE' : [game_patch_single_preprocessor]
    }
)

api = Api()


class Login(Resource):
    def post(self):

        email    = request.json.get("email")
        password = request.json.get("password")

        # missing arguments
        if email is None or password is None:
            abort(400, "Email or password is missing")

        user = User.query.filter_by(email = email).first()
        # this user does not exist
        if user is None:
            abort(400, "Non existent user '{}'".format(email))

        # Incorrect password
        if not user.verify_password(password):
            abort(400, "Wrong credentials")

        access_token  = create_access_token(identity = user.id)
        refresh_token = create_refresh_token(identity = user.id)

        res = make_response(jsonify({
            'access_token': access_token,
            'refresh_token': refresh_token,
            'message': 'Logged in as {}'.format(user.email),
            'user' : {
                'id'    : user.id,
                'email' : user.email,
                'name'  : user.name
            }
        }), 200)

        return res


class Token(Resource):
    @jwt_refresh_token_required
    def post(self):
        access_token = create_access_token(identity = get_jwt_identity())
        return make_response(jsonify({'access_token': access_token}),200)