from flask import Flask
import os
import sys
from flask_jwt_extended import JWTManager

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')

from app.api.v1.auth import create_admin


def create_app():
    """ create flask app"""
    app = Flask(__name__)
    from app import api_bp
    app.config['JWT_SECRET_KEY'] = "changing_soon"
    jwt = JWTManager(app)
    create_admin()
    app.register_blueprint(api_bp, url_prefix='/dann/api/v1')

    return app


application = create_app()

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 5000))
    application.run(port=PORT, debug=True)
