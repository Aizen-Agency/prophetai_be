from ..extensions import get_db_connection
from datetime import datetime

class Insights:
    def __init__(self, id=None, user_id=None, articles_scraped=0, videos_posted=0, created_at=None):
        self.id = id
        self.user_id = user_id
        self.articles_scraped = articles_scraped
        self.videos_posted = videos_posted
        self.created_at = created_at or datetime.now()

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS insights (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
                articles_scraped INTEGER DEFAULT 0,
                videos_posted INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """
        
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        conn.close()

    def save(self):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            INSERT INTO insights (user_id, articles_scraped, videos_posted, created_at)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (self.user_id, self.articles_scraped, self.videos_posted, self.created_at))
        
        self.id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        conn = get_db_connection()
        cur = conn.cursor()
        
        cur.execute("""
            UPDATE insights
            SET articles_scraped = %s,
                videos_posted = %s
            WHERE id = %s
        """, (self.articles_scraped, self.videos_posted, self.id))
        
        conn.commit()
        cur.close()
        conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM insights WHERE user_id = %s", (user_id,))
        insights_data = cur.fetchone()
        cur.close()
        conn.close()
        if insights_data:
            return Insights(**insights_data)
        return None

    def __repr__(self):
        return f"<Insights {self.id} | User {self.user_id}>"

# If going for montly insights

# class MonthlyInsights(db.Model):
#     __tablename__ = 'monthly_insights'

#     id = db.Column(Integer, primary_key=True)
#     user_id = db.Column(Integer, ForeignKey('userData.id'), nullable=False)

#     month = db.Column(String(10), nullable=False)  # e.g. 'Jan'
#     year = db.Column(Integer, nullable=False)

#     articles = db.Column(Integer, default=0)
#     scripts = db.Column(Integer, default=0)
#     short_videos = db.Column(Integer, default=0)
#     long_videos = db.Column(Integer, default=0)
#     total_videos = db.Column(Integer, default=0)

#     created_at = db.Column(DateTime, server_default=func.now())
