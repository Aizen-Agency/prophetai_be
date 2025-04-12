from ..extensions import db
from sqlalchemy import Integer, String, DateTime, func

class User(db.Model):
    __tablename__ = 'userData'

    id = db.Column(Integer, primary_key=True)
    firstname = db.Column(String(50), nullable=False)
    lastname = db.Column(String(50), nullable=False)
    phoneNo = db.Column(String(15), nullable=False)
    email = db.Column(String(100), unique=True, nullable=False)
    password = db.Column(String(100), nullable=False)
    created_at = db.Column(DateTime, server_default=func.now())

    def __repr__(self):
        return f"<User {self.id} | {self.email}>"
