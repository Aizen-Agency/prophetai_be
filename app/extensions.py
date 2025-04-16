import psycopg2
from psycopg2.extras import RealDictCursor
import os

def get_db_connection():
    try:
        conn = psycopg2.connect(
            os.getenv('DATABASE_URL'),
            cursor_factory=RealDictCursor
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {str(e)}")
        raise 