from flask import Blueprint
from flask_restful import Api

# local imports
from app.api.v1.sales_view import Records


api_bp = Blueprint('api', __name__)
api = Api(api_bp)

# Routes
api.add_resource(Records, '/sales')
