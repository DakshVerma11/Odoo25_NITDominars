from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions with app
    db.init_app(app)
    
    # Register middleware
    from app.middleware import register_middleware
    register_middleware(app)
    
    # Register blueprints
    from app.routes import register_blueprints
    register_blueprints(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Create all tables if they don't exist
    with app.app_context():
        db.create_all()
    
    return app