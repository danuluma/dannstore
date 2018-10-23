from flask import Flask
from flask import Blueprint
from flask_restful import Api
from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
import os
import sys


LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/')
# Local imports now

from app.api.v1.auth import create_admin
from app.api.v2.db import Db
from app.api.v2.models.user import UserModel
from config import app_config
from app.api.v1.sales_view import Records, SingleRecord
from app.api.v1.products_view import Home, Products, SingleProduct
from app.api.v1.auth import Register, Login
from app.api.v2.views.users import Register as R2, Login as L2, User, Users, Logout

load_dotenv()


api_bp = Blueprint('api', __name__)
api_bp2 = Blueprint('api2', __name__)
api = Api(api_bp)
api2 = Api(api_bp2)

# Routes
api.add_resource(Home, '/home')
api.add_resource(Products, '/products')
api.add_resource(SingleProduct, '/products/<int:productID>')
api.add_resource(Register, '/reg')
api.add_resource(Login, '/login')
api.add_resource(Records, '/sales')
api.add_resource(SingleRecord, '/sales/<int:saleID>')
api2.add_resource(R2, '/reg')
api2.add_resource(L2, '/login')
api2.add_resource(User, '/users/<int:userID>')
api2.add_resource(Users, '/users')
api2.add_resource(Logout, '/logout')


def create_app(config_name):
    """ create flask app"""
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    from app import api_bp, api_bp2
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    jwt = JWTManager(app)

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        """Checks if token is blacklisted"""
        jti = decrypted_token['jti']
        return jti in UserModel().blacklisted_tokens()
    create_admin()
    # Db().drop()
    Db().create()
    app.register_blueprint(api_bp, url_prefix='/dann/api/v1')
    app.register_blueprint(api_bp2, url_prefix='/dann/api/v2')

    return app
