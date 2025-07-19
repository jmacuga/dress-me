import os
from dotenv import load_dotenv

load_dotenv(override=True)


class Config:
    DEBUG = True
    SECRET_KEY = "aaaaaaaaasecret"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/app_db"


class ConfigTest:
    DEBUG = True
    SECRET_KEY = "aaaaaaaaasecret"
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@localhost:{os.getenv('DB_PORT')}/app_db"
