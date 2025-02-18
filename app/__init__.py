from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask("UniVerse")
    
    # Application configuration
    app.config['SECRET_KEY'] = ''  
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///universe.db'  # Using SQLite for simplicity
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with the app instance
    db.init_app(app)
    
    # Register Blueprints: This assumes you have a blueprint defined in routes.py
    from .routes import main
    app.register_blueprint(main)
    
    return app
