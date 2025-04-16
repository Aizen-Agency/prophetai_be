from ..extensions import get_db_connection
from datetime import datetime

class Insights:
    def __init__(self, id=None, user_id=None, **kwargs):
        self.id = id
        self.user_id = user_id
        
        # Initialize all monthly metrics with default values
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                 'july', 'august', 'september', 'october', 'november', 'december']
        metrics = ['articles', 'scripts', 'videos_generated', 'videos_posted']
        
        for month in months:
            for metric in metrics:
                attr_name = f"{month}_{metric}"
                setattr(self, attr_name, kwargs.get(attr_name, 0))

    @staticmethod
    def create_table():
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Create the table with all monthly metrics
        create_table_sql = """
            CREATE TABLE IF NOT EXISTS insights (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL,
        """
        
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                 'july', 'august', 'september', 'october', 'november', 'december']
        metrics = ['articles', 'scripts', 'videos_generated', 'videos_posted']
        
        for month in months:
            for metric in metrics:
                create_table_sql += f"{month}_{metric} INTEGER DEFAULT 0,\n"
        
        create_table_sql = create_table_sql.rstrip(',\n') + "\n)"
        
        cur.execute(create_table_sql)
        conn.commit()
        cur.close()
        conn.close()

    def save(self):
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Prepare column names and values
        columns = ['user_id']
        values = [self.user_id]
        
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                 'july', 'august', 'september', 'october', 'november', 'december']
        metrics = ['articles', 'scripts', 'videos_generated', 'videos_posted']
        
        for month in months:
            for metric in metrics:
                attr_name = f"{month}_{metric}"
                columns.append(attr_name)
                values.append(getattr(self, attr_name))
        
        placeholders = ', '.join(['%s'] * len(values))
        column_names = ', '.join(columns)
        
        cur.execute(f"""
            INSERT INTO insights ({column_names})
            VALUES ({placeholders})
            RETURNING id
        """, values)
        
        self.id = cur.fetchone()['id']
        conn.commit()
        cur.close()
        conn.close()

    def update(self):
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Prepare update statement
        updates = []
        values = []
        
        months = ['january', 'february', 'march', 'april', 'may', 'june', 
                 'july', 'august', 'september', 'october', 'november', 'december']
        metrics = ['articles', 'scripts', 'videos_generated', 'videos_posted']
        
        for month in months:
            for metric in metrics:
                attr_name = f"{month}_{metric}"
                updates.append(f"{attr_name} = %s")
                values.append(getattr(self, attr_name))
        
        values.append(self.id)
        update_str = ', '.join(updates)
        
        cur.execute(f"""
            UPDATE insights
            SET {update_str}
            WHERE id = %s
        """, values)
        
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

    def get_monthly_data(self, month):
        """Get all metrics for a specific month"""
        metrics = ['articles', 'scripts', 'videos_generated', 'videos_posted']
        return {
            metric: getattr(self, f"{month}_{metric}")
            for metric in metrics
        }

    def update_monthly_data(self, month, data):
        """Update metrics for a specific month"""
        for metric, value in data.items():
            setattr(self, f"{month}_{metric}", value)
        self.update()

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
