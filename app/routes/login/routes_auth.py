import os
import uuid
from random import choice
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from app.extensions import db
from app.models.userData import User
import jwt
from datetime import datetime, timedelta

load_dotenv()

api_login = Blueprint("login", __name__, url_prefix="")


@api_login.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate request data
        if not data:
            return jsonify({"error": "No data provided"}), 400
            
        # Extract and validate required fields
        required_fields = ['email', 'password', 'phoneNo', 'firstname', 'lastname']
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing or empty required field: {field}"}), 400

        email = data['email'].strip().lower()
        password = data['password']
        phoneNo = data['phoneNo'].strip()
        firstname = data['firstname'].strip()
        lastname = data['lastname'].strip()

        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400

        # Validate password strength
        if len(password) < 8:
            return jsonify({"error": "Password must be at least 8 characters long"}), 400

        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({"error": "Email already registered"}), 409

        # Hash password
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        # Create new user
        new_user = User(
            email=email,
            password=hashed_password,
            phoneNo=phoneNo,
            firstname=firstname,
            lastname=lastname
        )

        # Add to database
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "User created successfully",
            "user": {
                "email": email,
                "firstname": firstname,
                "lastname": lastname
            }
        }), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        print(f"[SQLAlchemyError] {str(e)}") 
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        print(f"[ERROR] {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500



@api_login.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate request data
        if not data:
            return jsonify({"error": "No data provided"}), 400

        # Validate required fields
        if 'email' not in data or 'password' not in data:
            return jsonify({"error": "Missing email or password"}), 400

        email = data['email'].strip().lower()
        password = data['password']

        # Check for admin credentials
        if email == os.getenv('ADMIN_EMAIL') and password == os.getenv('ADMIN_PASSWORD'):
            return jsonify({
                "message": "Welcome Admin!",
                "user": {
                    "email": email,
                    "isAdmin": True
                },
                "success": True
            }), 200

        # Validate email format
        if '@' not in email or '.' not in email:
            return jsonify({"error": "Invalid email format"}), 400

        # Find user
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({"error": "Email not found"}), 401

        # Verify password
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Wrong password"}), 401

        return jsonify({
            "message": f"Welcome {user.firstname}!",
            "user": {
                "id": user.id,
                "firstname": user.firstname,
                "lastname": user.lastname,
                "email": user.email,
                "isAdmin": False
            },
            "success": True
        }), 200

    except SQLAlchemyError as e:
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred"}), 500

