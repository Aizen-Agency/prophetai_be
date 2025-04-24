import os
from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from app.models.userData import User
from app.extensions import get_db_connection
import jwt
from datetime import datetime, timedelta
import psycopg2.extras
from app.models.insights import Insights

load_dotenv()

api_login = Blueprint("login", __name__, url_prefix="")

def get_user_by_email(email):
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cur.execute("SELECT * FROM userData WHERE email = %s", (str(email),))
        user_data = cur.fetchone()
        cur.close()
        conn.close()
        if user_data:
            return User(**user_data)
        return None
    except Exception as e:
        print(f"Error getting user by email: {str(e)}")
        raise

@api_login.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        required_fields = ['firstname', 'lastname', 'phoneNo', 'email', 'password']
        for field in required_fields:
            if field not in data or not isinstance(data[field], str) or not data[field].strip():
                return jsonify({'error': f"Field '{field}' is required and must be a non-empty string"}), 400

        print("data present", data)

        # Check if user exists
        existing_user = get_user_by_email(data.get('email'))
        if existing_user:
            return jsonify({'error': 'User already exists'}), 400

        print("user not found")

        user = User(
            firstname=data['firstname'],
            lastname=data['lastname'],
            phoneNo=data['phoneNo'],
            email=data['email'],
            password=generate_password_hash(data['password'])
        )
        user.save()

        print("user saved")

        # Create a new insights record for the user
        insights = Insights(user_id=user.id)
        insights.save()

        print("insights record created")

        return jsonify({
            'message': 'User created successfully',
            'user': user.to_dict()
        }), 201

    except Exception as e:
        print("Error in signup:", str(e))
        return jsonify({'error': str(e)}), 500

@api_login.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'password' not in data:
            return jsonify({'error': 'Email and password are required'}), 400
        
        print("data present", data)

        # Check if credentials match admin credentials
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')
        is_admin = (data.get('email') == admin_email and data.get('password') == admin_password)
        if is_admin:
            return jsonify({
                'user': {
                    'email': admin_email,
                    'firstname': 'Admin',
                    'id': 0,
                    'isAdmin': True
                }
            }), 200 

        user = get_user_by_email(data.get('email'))
        if not user or not check_password_hash(user.password, data.get('password')):
            return jsonify({'error': 'Invalid email or password'}), 401
        
        print("user found", user)

        user_dict = user.to_dict()
        user_dict['isAdmin'] = is_admin

        return jsonify({
            'user': user_dict
        }), 200

    except Exception as e:
        print("Error in login:", str(e))
        return jsonify({'error': str(e)}), 500
