from flask import Flask
from flask_cors import CORS
from .config import DevelopmentConfig
from .models import db
from dotenv import load_dotenv
from app.models.userData import UserData
import os
from .routes import init_routes

def create_app():
    load_dotenv()
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    # CORS(app, resources={
    #     r"/*": {
    #         "origins": "*",
    #         "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    #         "allow_headers": ["Content-Type", "Authorization", "Accept", "Origin", "X-Requested-With"],
    #         "expose_headers": ["Content-Range", "X-Content-Range"],
    #         "supports_credentials": True,
    #         "max_age": 600,
    #         "send_wildcard": False
    #     }
    # })
    # CORS(app, 
    # resources={r"/*": {
    #     "origins": ["http://localhost:3000", "https://aizen-crm-frontend-hmci.vercel.app"],  # Specify exact origins
    #     "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    #     "allow_headers": ["Content-Type", "Authorization"],  # Added Authorization header
    #     "supports_credentials": True
    # }})

    app.config.from_object(DevelopmentConfig)  # Load development config

    db.init_app(app)

    # Register all blueprints
    init_routes(app)

    # with app.app_context():
    #     UserData.__table__.create(db.engine, checkfirst=True)

    return app

app = create_app()




