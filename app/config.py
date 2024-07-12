# /app/config.py
import os
import secrets


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', secrets.token_hex(16))
    #the below code is bad practice
    #SECRET_KEY = 'e8be6c76f90f01893eedc58ee07c65fcc1e4339b1a854dc1edc9969402a84bc2'
    SQLALCHEMY_DATABASE_URI = 'mysql://silver:Password_12345@localhost/contact'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = '/images'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB limit

    # Flask-Mail configuration
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'marwaasabon@gmail.com'
    MAIL_PASSWORD = 'kcybbulukyxkdxzo'
    MAIL_DEFAULT_SENDER = 'marwasabon@gmail.com'
