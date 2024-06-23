# /app/config.py

class Config:
    SECRET_KEY = 'e8be6c76f90f01893eedc58ee07c65fcc1e4339b1a854dc1edc9969402a84bc2'
    SQLALCHEMY_DATABASE_URI = 'mysql://silver:Password_12345@localhost/contact'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
