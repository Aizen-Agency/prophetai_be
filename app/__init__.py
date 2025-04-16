from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from dotenv import load_dotenv
import os
from .routes import init_routes
from .models import init_models

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}} , supports_credentials=True)
    
    app.config.from_object(DevelopmentConfig)  # Load development config

    # Register all blueprints
    init_routes(app)

    # Initialize database tables
    init_models()

    return app

app = create_app()

def drop_all_tables():
    """Drop all database tables."""
    with app.app_context():
        db.drop_all()




