from dotenv import load_dotenv

import os

load_dotenv()


class Config():
    DEBUG = False
    TESTING = False
    DB_URI = os.getenv("DEV_DBURI")

class ProductionConfig(Config):
    DB_URI = os.getenv("PROD_DBURI")

class DevelopmentConfig(Config):
    DEBUG = True
    DB_URI = os.getenv("DEV_DBURI")

class TestingConfig(Config):
    TESTING = True
    DB_URI = os.getenv("TEST_DBURI")



app_config = {
  "testing": TestingConfig,
  "development": DevelopmentConfig,
  "production": ProductionConfig
}
