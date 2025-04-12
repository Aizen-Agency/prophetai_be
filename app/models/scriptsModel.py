from ..extensions import db
from sqlalchemy import Integer, String, DateTime, func, Boolean, ForeignKey

class Script(db.Model):
    __tablename__ = 'scripts'

    id = db.Column(Integer, primary_key=True)  # script_id
    user_id = db.Column(Integer, ForeignKey('userData.id'), nullable=False)

    title = db.Column(String(255), nullable=False)
    content = db.Column(String, nullable=False)  # actual script text
    product_name = db.Column(String(255), nullable=True)

    created_at = db.Column(DateTime, server_default=func.now())
    is_locked = db.Column(Boolean, default=False)

    def __repr__(self):
        return f"<Script {self.id} | User {self.user_id} | Title: {self.title}>"
