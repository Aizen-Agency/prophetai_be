from . import db
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from datetime import datetime

class Insights(db.Model):
    __tablename__ = 'insights'

    id = db.Column(Integer, primary_key=True)
    
    # Foreign Key to UserData
    user_id = db.Column(Integer, ForeignKey('userData.id'), nullable=False)

    # Cumulative Metrics
    articles_scraped = db.Column(Integer, default=0)
    scripts_generated = db.Column(Integer, default=0)
    videos_generated = db.Column(Integer, default=0)
    videos_posted = db.Column(Integer, default=0)

    # Optional: Store current month's values for quick display
    month = db.Column(String(20), default=datetime.utcnow().strftime('%B'))
    year = db.Column(Integer, default=datetime.utcnow().year)

    # Timestamps
    created_at = db.Column(DateTime, server_default=func.now())
    updated_at = db.Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Insights user_id={self.user_id} month={self.month} year={self.year}>"


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
