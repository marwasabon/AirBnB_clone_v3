from app import db
from app.models.base_model import BaseModel
class User(BaseModel):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'User: [id: {}, username: {}, password: {}'.format(self.id, self.username, self.password)
