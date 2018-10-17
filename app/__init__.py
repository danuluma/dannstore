from flask import Blueprint
from flask_restful import Api

# local imports
from app.api.v1.sales_view import Records
from app.api.v1.products_view import Home, Products, SingleProduct
from app.api.v1.auth import Register, Login


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(Home, '/home')
api.add_resource(Products, '/products')
api.add_resource(SingleProduct, '/products/<int:productID>')
api.add_resource(Register, '/reg')
api.add_resource(Login, '/login')
api.add_resource(Records, '/sales')
