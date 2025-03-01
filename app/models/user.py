from app import db
from app.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from app.models.role import Role
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(255), nullable=False)
    email = Column(String(100), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    items = relationship('Item', back_populates='user')
    claims = relationship('Claim', back_populates='user')
    role_id = Column(Integer, ForeignKey('roles.id'))
    role = relationship('Role', backref='users')
    
    def __repr__(self):
        return 'User: [id: {}, username: {}, Email: {}, Profile_image: {}, role: {}'.format(self.id, self.username, self.email, self.image_file, self.role)
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def get_id(self):
        return str(self.id)
    
    def has_role(self, role_name):
        return self.role and self.role.name == role_name    
    @property
    def is_active(self):
        return True  # Example: Always return True for simplicity
   
    def __setattr__(self, name, value):
        """sets a password with md5 encryption"""
        if name == "password":
            value = generate_password_hash(value)
        super().__setattr__(name, value)
