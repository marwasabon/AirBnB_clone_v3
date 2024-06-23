from app import db
from app.models.base_model import BaseModel


class Contact(BaseModel):
    __tablename__ = 'contacts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    address = db.Column(db.String(255))
        
    def __repr__(self):
        return 'Contact: [id: {}, name: {}, address: {}]'.format(self.id, self.name, self.address)
