from flask import Flask, jsonify
from flask import Blueprint
from flask_restful import Api
import flask_restful
import os, sys
from flask_jwt_extended import JWTManager


# local imports
LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../')

from app.api.v1.auth import create_admin
from app.api.v1.sales_view import Records, SingleRecord
from app.api.v1.products_view import Home, Products, SingleProduct
from app.api.v1.auth import Register, Login


api_bp = Blueprint('api', __name__)
api = Api(api_bp)


# Add Routes
api.add_resource(Home, '/home')
api.add_resource(Products, '/products')
api.add_resource(SingleProduct, '/products/<int:productID>')
api.add_resource(Register, '/reg')
api.add_resource(Login, '/login')
api.add_resource(Records, '/sales')
api.add_resource(SingleRecord, '/sales/<int:saleID>')


def create_app():
    """ Create the Flask app"""

    app = Flask(__name__)
    app.config['JWT_SECRET_KEY'] = "changing_soon"
    jwt = JWTManager(app)
    create_admin()
    app.register_blueprint(api_bp, url_prefix='/dann/api/v1')

    @app.errorhandler(404)
    def not_found(error):
        """Resource not found error"""

        return jsonify({"Error": "Resource not found"}), 404

    @app.errorhandler(500)
    def server_error(error):
        """Server error"""

        return jsonify({"Error": "Internal server error"}), 500

    return app
