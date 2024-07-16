from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config  # Import the Config class
from .models.db_storage import DBStorage,db 
from .models.user import User
from flask_migrate import Migrate
from flask_login import LoginManager ,UserMixin
from flask_mail import Mail
import os

mail = Mail()
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)  # Apply configuration from Config class
    db.init_app(app)  # Initialize the global db instance with the app
    storage = DBStorage(db)
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'  # Set the login view for Flask-Login
    mail.init_app(app)
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    #migrate = Migrate(app, db)  # Initialize Flask-Migrate
    
    # Ensure the upload folder exists
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    from app.models.contact import Contact
    from app.models.role import Role
    from app.models.user import User
    from app.models.test import Test
    from app.models.item import Item
    from app.models.match import Match
    from app.models.claim import Claim
    from app.models.quality import QualityCheck
    from .main.routes import main as main_blueprint
    from .main.item_routes import item_bp as item_bp
    from .main.user_routes import user_bp as user_bp
    from .main.claim_routes import claim_bp as claim_bp
    from .main.match_routes import match_bp as match_bp
    app.register_blueprint(main_blueprint)
    app.register_blueprint(item_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(claim_bp)
    app.register_blueprint(match_bp)
    migrate = Migrate(app, db)
    return app
