from . import db
from sqlalchemy import Integer, String, ForeignKey, DateTime, func

class Video(db.Model):
    __tablename__ = 'videos'

    id = db.Column(Integer, primary_key=True)  # video_id
    user_id = db.Column(Integer, ForeignKey('userData.id'), nullable=False)

    name = db.Column(String(255), nullable=False)
    video_url = db.Column(String(1000), nullable=False)  # S3 link or CDN URL
    size = db.Column(String(100))  # e.g. "50MB"
    
    created_at = db.Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<Video {self.id} | User {self.user_id} | Name: {self.name}>"
