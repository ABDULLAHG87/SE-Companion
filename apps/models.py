# models.py
from secompanion import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy




class User(UserMixin, db.Model):
    __tablename__ = 'users'
    # this code below is for the sql command
    # id = Column(Integer, primary_key=True)
    # email = Column(String(100), unique=True, nullable=False)
    # password_hash = Column(String(256), nullable=False)
    
    #This code works for the mysql database
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # Increase the length of the column
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def __repr__(self):
        return f"{self.email}:{self.password_hash}"
