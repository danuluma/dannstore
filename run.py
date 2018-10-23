import os
import sys

LOCALPATH = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, LOCALPATH + '/')


from app import create_app


application = create_app()

if __name__ == "__main__":
    PORT = int(os.environ.get('PORT', 5000))
    application.run(port=PORT, debug=True)
