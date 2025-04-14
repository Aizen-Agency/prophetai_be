from ..extensions import db
from sqlalchemy import Integer, String, ForeignKey, DateTime, func
from datetime import datetime

class Insights(db.Model):
    __tablename__ = 'insights'

    id = db.Column(Integer, primary_key=True)
    
    # Foreign Key to UserData
    user_id = db.Column(Integer, ForeignKey('userData.id'), nullable=False)

    # Monthly Metrics for each month
    january_articles = db.Column(Integer, default=0)
    january_scripts = db.Column(Integer, default=0)
    january_videos_generated = db.Column(Integer, default=0)
    january_videos_posted = db.Column(Integer, default=0)

    february_articles = db.Column(Integer, default=0)
    february_scripts = db.Column(Integer, default=0)
    february_videos_generated = db.Column(Integer, default=0)
    february_videos_posted = db.Column(Integer, default=0)

    march_articles = db.Column(Integer, default=0)
    march_scripts = db.Column(Integer, default=0)
    march_videos_generated = db.Column(Integer, default=0)
    march_videos_posted = db.Column(Integer, default=0)

    april_articles = db.Column(Integer, default=0)
    april_scripts = db.Column(Integer, default=0)
    april_videos_generated = db.Column(Integer, default=0)
    april_videos_posted = db.Column(Integer, default=0)

    may_articles = db.Column(Integer, default=0)
    may_scripts = db.Column(Integer, default=0)
    may_videos_generated = db.Column(Integer, default=0)
    may_videos_posted = db.Column(Integer, default=0)

    june_articles = db.Column(Integer, default=0)
    june_scripts = db.Column(Integer, default=0)
    june_videos_generated = db.Column(Integer, default=0)
    june_videos_posted = db.Column(Integer, default=0)

    july_articles = db.Column(Integer, default=0)
    july_scripts = db.Column(Integer, default=0)
    july_videos_generated = db.Column(Integer, default=0)
    july_videos_posted = db.Column(Integer, default=0)

    august_articles = db.Column(Integer, default=0)
    august_scripts = db.Column(Integer, default=0)
    august_videos_generated = db.Column(Integer, default=0)
    august_videos_posted = db.Column(Integer, default=0)

    september_articles = db.Column(Integer, default=0)
    september_scripts = db.Column(Integer, default=0)
    september_videos_generated = db.Column(Integer, default=0)
    september_videos_posted = db.Column(Integer, default=0)

    october_articles = db.Column(Integer, default=0)
    october_scripts = db.Column(Integer, default=0)
    october_videos_generated = db.Column(Integer, default=0)
    october_videos_posted = db.Column(Integer, default=0)

    november_articles = db.Column(Integer, default=0)
    november_scripts = db.Column(Integer, default=0)
    november_videos_generated = db.Column(Integer, default=0)
    november_videos_posted = db.Column(Integer, default=0)

    december_articles = db.Column(Integer, default=0)
    december_scripts = db.Column(Integer, default=0)
    december_videos_generated = db.Column(Integer, default=0)
    december_videos_posted = db.Column(Integer, default=0)

    def __repr__(self):
        return f"<Insights user_id={self.user_id}>"

    def get_monthly_data(self, month):
        """Helper method to get data for a specific month"""
        month = month.lower()
        return {
            'articles': getattr(self, f'{month}_articles', 0),
            'scripts': getattr(self, f'{month}_scripts', 0),
            'videos_generated': getattr(self, f'{month}_videos_generated', 0),
            'videos_posted': getattr(self, f'{month}_videos_posted', 0)
        }

    def update_monthly_data(self, month, data):
        """Helper method to update data for a specific month"""
        month = month.lower()
        setattr(self, f'{month}_articles', data.get('articles', 0))
        setattr(self, f'{month}_scripts', data.get('scripts', 0))
        setattr(self, f'{month}_videos_generated', data.get('videos_generated', 0))
        setattr(self, f'{month}_videos_posted', data.get('videos_posted', 0))

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
