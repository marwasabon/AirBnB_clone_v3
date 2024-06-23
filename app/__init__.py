from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config  # Import the Config class
from .models.db_storage import DBStorage, db
from flask_migrate import Migrate
def create_app():

    app = Flask(__name__)
    app.config.from_object(Config)  # Apply configuration from Config class
    db.init_app(app)  # Initialize the global db instance with the app
    storage = DBStorage(db)
    #migrate = Migrate(app, db)  # Initialize Flask-Migrate
    from app.models.contact import Contact
    from app.models.user import User
    from app.models.test import Test
    from .main.routes import main as main_blueprint
    app.register_blueprint(main_blueprint)
    return app
