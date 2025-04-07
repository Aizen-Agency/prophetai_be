import os
import uuid
from random import choice
from flask import Blueprint, Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv
from app.models import db
from app.models.userData import UserData
import jwt
from datetime import datetime, timedelta

load_dotenv()

api_login = Blueprint("login", __name__, url_prefix="")






@api_login.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')
    phoneNo = data.get('phoneNo')
    firstname = data.get('firstname')
    lastname = data.get('lastname')

    if not email or not password or not phoneNo or not firstname or not lastname:
        return jsonify({"error": "Missing required fields"}), 400

    if UserData.query.filter_by(email=email).first():
        print("Email already exists")
        return jsonify({"error": "Email already registered"}), 400

    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    new_user = UserData(
        email=email,
        password=hashed_password,
        phoneNo=phoneNo,
        firstname=firstname,
        lastname=lastname
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201



@api_login.route('/login', methods=['POST'])
def login():
    print("Login route accessed")
    data = request.get_json()
    print(f"Received data: {data}")

    email = data['email']
    password = data['password']
    print(f"Attempting login for user: {email}")

    user = UserData.query.filter_by(email=email).first()
    print(f"User found: {user is not None}")

    if not user or not check_password_hash(user.password, password):
        print("Invalid username or password")
        return jsonify({"error": "Invalid username or password"}), 400

    print("Login successful")

    return jsonify({
        "message": f"Welcome {user.firstname}!",
        "firstname": user.firstname,
        "success": True,
    }), 200



# @api_login.route('/api/user-dashboard/<username>', methods=['GET'])
# def get_user_dashboard_data(username):
#     try:
#         # Get user
#         user = User.query.filter_by(username=username).first()
#         if not user:
#             return jsonify({"error": "User not found"}), 404
            
#         # Get agents
#         agents = Agent.query.filter_by(user_id=user.id).all()
        
#         # Get phone numbers
#         phone_numbers = PhoneNumber.query.filter_by(user_id=user.id).all()
        
#         return jsonify({
#             "user": {
#                 "username": user.username,
#                 "email": user.email,
#                 "parent_username": user.parent_username,
#                 "is_subaccount": user.is_subaccount,
#                 "created_at": user.created_at.isoformat() if hasattr(user, 'created_at') else None
#             },
#             "agents": [{
#                 "id": agent.id,
#                 "description": agent.description,
#                 "website": agent.website,
#                 "created_at": agent.created_at.isoformat()
#             } for agent in agents],
#             "phone_numbers": [{
#                 "id": number.id,
#                 "phone_number": number.phone_number,
#                 "country": number.country,
#                 "created_at": number.timestamp.isoformat()
#             } for number in phone_numbers]
#         }), 200
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500