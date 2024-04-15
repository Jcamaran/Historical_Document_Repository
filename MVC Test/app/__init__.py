# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy here

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = 'uploaded_documents'
    
    db.init_app(app)  # Initialize 'db' with the Flask app context here

    from .routes import app_views  # Use relative import for the Blueprint
    app.register_blueprint(app_views)
    
    return app
