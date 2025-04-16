from ..extensions import get_db_connection
from datetime import datetime

class Script:
    def __init__(self, id=None, user_id=None, title=None, content=None, is_idea=False, created_at=None, updated_at=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.content = content
        self.is_idea = is_idea
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS scripts (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                title VARCHAR(255) NOT NULL,
                content TEXT NOT NULL,
                is_idea BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)
        conn.commit()
        cur.close()
        conn.close()

    def save(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO scripts (user_id, title, content, is_idea, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (self.user_id, self.title, self.content, self.is_idea, self.created_at))
        self.id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE scripts
            SET content = %s, updated_at = %s
            WHERE id = %s
        """, (self.content, self.updated_at, self.id))
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_by_user_and_title(user_id, title):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM scripts
            WHERE user_id = %s AND title = %s
        """, (user_id, title))
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
        return f"<Script {self.id} | {self.title}>"
