from app import db
from app.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from hashlib import md5

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100), nullable=False)
    email = Column(String(100), nullable=False)
    items = relationship('Item', back_populates='user')
    claims = relationship('Claim', back_populates='user')
    
    def __repr__(self):
        return 'User: [id: {}, username: {}, Email: {}'.format(self.id, self.username, self.email)
    
    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = md5(value.encode()).hexdigest()
        super().__setattr__(name, value)
