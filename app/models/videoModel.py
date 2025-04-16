from ..extensions import get_db_connection
from datetime import datetime

class Video:
    def __init__(self, id=None, user_id=None, script_id=None, video_url=None, size=None, created_at=None):
        self.id = id
        self.user_id = user_id
        self.script_id = script_id
        self.video_url = video_url
        self.size = size
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                script_id INTEGER NOT NULL,
                video_url VARCHAR(1000) NOT NULL,
                size VARCHAR(100),
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
            INSERT INTO videos (user_id, script_id, video_url, size, created_at)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (self.user_id, self.script_id, self.video_url, self.size, self.created_at))
        self.id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_by_id(video_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM videos WHERE id = %s", (video_id,))
        video_data = cur.fetchone()
        cur.close()
        conn.close()
        if video_data:
            return Video(**video_data)
        return None

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM videos WHERE user_id = %s", (user_id,))
        videos = [Video(**video_data) for video_data in cur.fetchall()]
        cur.close()
        conn.close()
        return videos

    def __repr__(self):
        return f"<Video {self.id} | User {self.user_id} | Script {self.script_id}>"
