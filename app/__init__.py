from flask import Blueprint
from flask_restful import Api

# local imports
from app.api.v1.sales_view import Records, SingleRecord
from app.api.v1.products_view import Home, Products, SingleProduct
from app.api.v1.auth import Register, Login
from app.api.v2.views.users import Register as R2, Login as L2, User, Users, Logout


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
