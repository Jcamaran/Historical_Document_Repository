from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Initialize SQLAlchemy here

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///documents.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['UPLOAD_FOLDER'] = r'C:\\Users\\mahmu\Downloads\\MVC Test\\app\static\\uploaded_documents'  # Ensure this path is correct

    db.init_app(app)  # Initialize 'db' with the Flask app context here

    from .models import Document  # noqa: F401

    with app.app_context():
        db.create_all()  # Create database tables

    from .routes import app_views  # Import routes after db initialization
    app.register_blueprint(app_views)

    return app
