from app import db
from app.models.base_model import BaseModel
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum
from datetime import datetime
from sqlalchemy.orm import relationship

class Item(db.Model):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)  
    name = Column(String(80), nullable=True)  
    email = Column(String(120), nullable=False)  
    phone = Column(String(15), nullable=False)  
    item_name = Column(String(80), nullable=False)  
    item_category = Column(String(50), nullable=False)  
    item_color = Column(String(50), nullable=False)  
    item_brand = Column(String(50), nullable=True)  
    date_lost_found = Column(DateTime, nullable=True)  
    location_lost_found = Column(String(255), nullable=False)  
    image_url = Column(String(255), nullable=True)  
    description = Column(String(255), nullable=False)  
    category = Column(String(50), nullable=True)  
    status = Column(Enum('Lost', 'Found', 'Report', 'Closed',name='status_types'), nullable=False, default='Lost')  
    date_reported = Column(DateTime, default=datetime.utcnow)  
    user_id = Column(Integer, ForeignKey('users.id'))  
    user = relationship('User', back_populates='items')  
    claims = relationship('Claim', back_populates='item')  
    matches = relationship('Match', back_populates='item')  