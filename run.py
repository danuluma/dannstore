import os
import sys


LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/')
# Local imports now

from app import create_app


application = create_app(os.getenv('APP_SETTINGS'))

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 5000))
    application.run(port=PORT, debug=True)
