from flask import Flask, jsonify, redirect
from flask import Blueprint
from flask_restful import Api
import flask_restful
import os, sys
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv


# local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../')

from app.api.v1.auth import create_admin
from app.api.v1.sales_view import Records, SingleRecord
from app.api.v1.products_view import Home, Products, SingleProduct
from app.api.v1.auth import Register, Login
from app.api.v2.views.users import Register as R2, Login as L2, User, Users, Logout
from app.api.v2.db import Db
from app.api.v2.models.user import UserModel
from config import app_config
from app.api.v2.views.products import Products as P2, SingleProduct as S2
from app.api.v2.views.sales import Records as SR2, SingleRecord as SR3

load_dotenv()


api_bp = Blueprint('api', __name__)
api_bp2 = Blueprint('api2', __name__)
api = Api(api_bp)
api2 = Api(api_bp2)


# Add Routes
api.add_resource(Home, '/home')
api.add_resource(Products, '/products')
api.add_resource(SingleProduct, '/products/<int:productID>')
api.add_resource(Register, '/reg')
api.add_resource(Login, '/login')
api.add_resource(Records, '/sales')
api.add_resource(SingleRecord, '/sales/<int:saleID>')
api2.add_resource(R2, '/signup')
api2.add_resource(L2, '/login')
api2.add_resource(User, '/users/<int:userID>')
api2.add_resource(Users, '/users')
api2.add_resource(Logout, '/logout')
api2.add_resource(P2, '/products')
api2.add_resource(SR2, '/sales')
api2.add_resource(S2, '/products/<int:productID>')
api2.add_resource(SR3, '/sales/<int:saleID>')


def create_app(config_name):
    """Create the flask app."""

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
    Db().drop()
    Db().create()
    app.register_blueprint(api_bp, url_prefix='/dann/api/v1')
    app.register_blueprint(api_bp2, url_prefix='/dann/api/v2')

    @app.errorhandler(500)
    def server_error(error):
        """Handle server error"""

        return jsonify({"Error": "Internal server error"}), 500

    @app.errorhandler(404)
    def not_found(error):
        """Handle resource not found error"""

        return jsonify({"Error": "Resource not found"}), 404
    @app.route('/')
    def root():
        return redirect('https://documenter.getpostman.com/view/5303933/RWgxvvVD')

    return app
