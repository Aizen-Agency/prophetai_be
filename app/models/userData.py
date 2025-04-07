from . import db
from sqlalchemy import Boolean, String, Text, ForeignKey, func, Integer, DateTime
from datetime import datetime


class UserData(db.Model):

    __tablename__ = 'userData' 
     
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    phoneNo = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
