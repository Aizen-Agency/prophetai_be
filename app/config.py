# Database Management 

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')  # Changed to use DATABASE_URL from Heroku


class DevelopmentConfig(Config):
    DEBUG = True
    # Heroku Postgres automatically provides DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

class ProductionConfig(Config):
    DEBUG = False
    # SQLALCHEMY_DATABASE_URI for production DB