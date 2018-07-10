from flask import Flask
from flask_cors import CORS
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

import data.mongo_setup as mongo_setup
import logging

app = Flask(__name__, static_url_path='/static')
handler = logging.FileHandler('inmuebles-crud.log')
handler.setLevel(logging.DEBUG)
app.logger.addHandler(handler)

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


from web_rest import user_auth_resource, inmueble_resource, foto_resource
from web_static import static_file_server
from data_auth import models

api.add_resource(user_auth_resource.UserRegistration, '/api/registration')
api.add_resource(user_auth_resource.UserLogin, '/api/login')
api.add_resource(user_auth_resource.UserAccount, '/api/account')
api.add_resource(user_auth_resource.UserLogoutAccess, '/api/logout/access')
api.add_resource(user_auth_resource.UserLogoutRefresh, '/api/logout/refresh')
api.add_resource(user_auth_resource.TokenRefresh, '/api/token/refresh')
api.add_resource(user_auth_resource.AllUsers, '/api/users')

api.add_resource(inmueble_resource.AgregarInmueble, '/api/inmueble')
api.add_resource(inmueble_resource.ObtenerTodosLosInmuebles, '/api/inmueble')
api.add_resource(inmueble_resource.BorrarInmueble, '/api/inmueble/<string:inmueble_id>')
api.add_resource(inmueble_resource.EditarInmueble, '/api/inmueble')

# api.add_resource(foto_resource.FotoCollection, '/api/foto')
# api.add_resource(foto_resource.FotoItem, '/api/foto/<string:foto_id>')
# api.add_resource(foto_resource.FotoItemByInmueble, '/api/fotos_inmueble/<string:inmueble_id>')

api.add_resource(static_file_server.UploadFoto, '/api/foto/upload')


@app.before_first_request
def create_tables():
    db.create_all()
    mongo_setup.global_init()
