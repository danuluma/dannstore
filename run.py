from flask import Flask
import os, sys

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/../../../')


def create_app():
    """ create flask app"""
    app = Flask(__name__)
    from app import api_bp
    app.register_blueprint(api_bp, url_prefix='/dann/api/v1')

    return app


application = create_app()

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 5000))
    application.run(port=PORT, debug=True)
