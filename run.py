from flask import Flask
import os
import sys
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv


LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/')
# Local imports now

from app.api.v1.auth import create_admin
from app.api.v2.db import Db
from app.api.v2.models.user import UserModel
from config import app_config

load_dotenv()


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


application = create_app(os.getenv('APP_SETTINGS'))

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 5000))
    application.run(port=PORT, debug=True)
