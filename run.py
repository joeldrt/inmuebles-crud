from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import data.mongo_setup as mongo_setup

app = Flask(__name__)
CORS(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '32SsNeiy'

db = SQLAlchemy(app)

app.config['JWT_SECRET_KEY'] = '32SsNeiy'
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return models.RevokedTokenModel.is_jti_blacklisted(jti)


from web_rest import user_auth_resource, inmueble_resource
import models

api.add_resource(user_auth_resource.UserRegistration, '/registration')
api.add_resource(user_auth_resource.UserLogin, '/login')
api.add_resource(user_auth_resource.UserLogoutAccess, '/logout/access')
api.add_resource(user_auth_resource.UserLogoutRefresh, '/logout/refresh')
api.add_resource(user_auth_resource.TokenRefresh, '/token/refresh')
api.add_resource(user_auth_resource.AllUsers, '/users')
api.add_resource(user_auth_resource.SecretResource, '/secret')

api.add_resource(inmueble_resource.InmuebleAgregar, '/inmueble')
api.add_resource(inmueble_resource.ObtenerTodosLosInmuebles, '/inmuebles')


@app.before_first_request
def create_tables():
    db.create_all()
    mongo_setup.global_init()
