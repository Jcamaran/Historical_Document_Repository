from flask import Flask
from app.routes import bp as routes_bp
from app.models import db

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'secretkey'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Historical_Database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(routes_bp)

    return app
