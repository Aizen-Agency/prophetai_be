from ..extensions import get_db_connection
from datetime import datetime
import uuid

class Script:
    def __init__(self, id=None, user_id=None, idea_id=None, idea_title=None, script_title=None, script_content=None, is_locked=False, created_at=None):
        self.id = id
        self.user_id = user_id
        self.idea_id = idea_id
        self.idea_title = idea_title
        self.script_title = script_title
        self.script_content = script_content
        self.is_locked = is_locked
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scripts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                idea_id UUID NOT NULL,
                idea_title VARCHAR(255) NOT NULL,
                script_title VARCHAR(255) NOT NULL,
                script_content TEXT NOT NULL,
                is_locked BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

    def save(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scripts (user_id, idea_id, idea_title, script_title, script_content, is_locked, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (self.user_id, self.idea_id, self.idea_title, self.script_title, self.script_content, self.is_locked, self.created_at))
        self.id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE scripts
            SET script_content = %s, is_locked = %s
            WHERE id = %s
        """, (self.script_content, self.is_locked, self.id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_by_user_and_idea_id(user_id, idea_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM scripts
            WHERE user_id = %s AND idea_id = %s
        """, (user_id, idea_id))
        script_data = cur.fetchone()
        cur.close()
        conn.close()
        if script_data:
            return Script(**script_data)
        return None

    @staticmethod
    def get_by_id_and_user(script_id, user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM scripts
            WHERE idea_id = %s AND user_id = %s
        """, (script_id, user_id))
        script_data = cur.fetchone()
        cur.close()
        conn.close()
        if script_data:
            return Script(**script_data)
        return None

    @staticmethod
    def delete(script_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM scripts WHERE id = %s", (script_id,))
        conn.commit()
        cur.close()
        conn.close()

    def __repr__(self):
        return f"<Script {self.id} | {self.script_title}>"
