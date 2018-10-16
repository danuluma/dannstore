from flask import Blueprint
from flask_restful import Api

# local imports
from app.api.v1.views import Home, Products, SingleProduct


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(Home, '/home')
api.add_resource(Products, '/products')
api.add_resource(SingleProduct, '/products/<int:productID>')

