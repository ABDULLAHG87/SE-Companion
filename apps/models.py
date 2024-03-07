from flask_login import UserMixin
from secompanion import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# Many-to-Many association tables
interests_association = db.Table('interests_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('interest_id', db.Integer, db.ForeignKey('interest.id'))
)

skills_association = db.Table('skills_association',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('skill_id', db.Integer, db.ForeignKey('skill.id'))
)

class User(UserMixin, db.Model):
    '''Declaration of user class inherited from db.Model and Flask-Login's UserMixin'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    sex = db.Column(db.String(10))
    city = db.Column(db.String(50))
    state = db.Column(db.String(50))
    country = db.Column(db.String(50))
    github_link = db.Column(db.String(256))
    linkedin_link = db.Column(db.String(256))
    twitter_link = db.Column(db.String(256))
    resume_link = db.Column(db.String(256))
    interests = db.relationship('Interest', secondary=interests_association, backref='users_interests')
    skills = db.relationship('Skill', secondary=skills_association, backref='users')
    avatar_image = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __init__(self, username, email, password):
        '''Method to initialize user object with username, email and password'''
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def set_password(self, password):
        '''Method to set password hash'''
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        '''Method to check password against password hash'''
        return check_password_hash(self.password_hash, password)

class Interest(db.Model):
    '''Declaration of interests class inherited from db.model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)
    users = db.relationship('User', secondary=interests_association, backref='user_interests')
    
class Skill(db.Model):
    '''Declaration of skills class inherited from db.model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, index=True)

class Resource(db.Model):
    '''Declaration of resources class inherited from db.model'''
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), index=True)
    description = db.Column(db.Text)
    type = db.Column(db.String(50))
    category = db.Column(db.String(50))
    level = db.Column(db.String(50))
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Tool(db.Model):
    '''Declaration of tool class inherited from db.model'''
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True)
    description = db.Column(db.Text)
    link = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Connection(db.Model):
    '''Declaration of connection class inherited from db.model'''
    id = db.Column(db.Integer, primary_key=True)
    user1_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user2_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.String(20))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Admin(db.Model):
    '''Declaration of admin class inherited from db.model'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(256))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
