from app import db
from app.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from sqlalchemy.orm import relationship

class Match(db.Model):
    __tablename__ = 'matches'
    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, ForeignKey('items.id'))
    potential_owner_user_id = Column(Integer, ForeignKey('users.id'))
    item = relationship('Item', back_populates='matches')
    quality_checks = relationship('QualityCheck', back_populates='match')
    status = db.Column(db.String(50), nullable=False, default='pending')
    #claim = relationship('Claim', back_populates='matches')
    claim_id = Column(Integer, ForeignKey('claims.id'))  # Add claim_id field
