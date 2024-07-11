from app import db
from app.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime

class Claim(db.Model):
    __tablename__ = 'claims'
    id = Column(Integer, primary_key=True)
    date_claimed = Column(DateTime, default=datetime.utcnow)
    additional_information = Column(String(255))
    status = db.Column(db.String(50), nullable=False, default='pending')
    item_id = Column(Integer, ForeignKey('items.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    item = relationship('Item', back_populates='claims')
    user = relationship('User', back_populates='claims')
    #matches = relationship('Match', back_populates='claims')
