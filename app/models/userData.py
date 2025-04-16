from ..extensions import get_db_connection
from datetime import datetime
import psycopg2

class User:
    def __init__(self, id=None, firstname=None, lastname=None, phoneNo=None, phoneno=None, email=None, password=None, created_at=None):
        try:
            self.id = int(id) if id is not None else None
            self.firstname = str(firstname) if firstname is not None else None
            self.lastname = str(lastname) if lastname is not None else None
            self.phoneNo = str(phoneNo or phoneno) if (phoneNo or phoneno) is not None else None
            self.email = str(email) if email is not None else None
            self.password = str(password) if password is not None else None
            self.created_at = created_at or datetime.now()
        except Exception as e:
            raise ValueError(f"Error initializing User: {str(e)}")

    @staticmethod
    def create_table():
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS userData (
                    id SERIAL PRIMARY KEY,
                    firstname VARCHAR(50) NOT NULL,
                    lastname VARCHAR(50) NOT NULL,
                    phoneNo VARCHAR(15) NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("User table created successfully")
        except Exception as e:
            print(f"Error creating user table: {str(e)}")
            raise

    def save(self):
        try:
            required_fields = {
                'firstname': self.firstname,
                'lastname': self.lastname,
                'phoneNo': self.phoneNo,
                'email': self.email,
                'password': self.password
            }

            for field, value in required_fields.items():
                if not isinstance(value, str):
                    raise ValueError(f"Field {field} must be a string, got {type(value)}")
                if not value.strip():
                    raise ValueError(f"Field {field} cannot be empty")

            conn = get_db_connection()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            try:
                cur.execute("""
                    INSERT INTO userData (firstname, lastname, phoneNo, email, password)
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    self.firstname,
                    self.lastname,
                    self.phoneNo,
                    self.email,
                    self.password
                ))
                result = cur.fetchone()
                if result and 'id' in result:
                    self.id = int(result['id'])
                conn.commit()
            finally:
                cur.close()
                conn.close()
        except Exception as e:
            print(f"Error saving user: {str(e)}")
            raise ValueError(f"Error saving user: {str(e)}")

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'phoneNo': self.phoneNo,
            'email': self.email,
            'created_at': self.created_at
        }

    def __repr__(self):
        return f"<User {self.id} | {self.email}>"
