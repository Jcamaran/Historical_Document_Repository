# pylint: disable=unused-function
from flask import Flask
from .extensions import db, login_manager
from .models import User, db
from .routes import app_views  # Make sure this import is correct
from .auth import auth as auth_blueprint
from typing import Any



def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'very_secret_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///yourdatabase.db'
    app.config['UPLOAD_FOLDER'] = r'C:\\Users\\mahmu\Downloads\\Historical_Document_Repository-main\\Historical_Document_Repository-main\\MVC Test\\app\static\\uploaddoc'  # Ensure this path is correct


    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(app_views, url_prefix='/')

    with app.app_context():
        db.create_all()  # This will create all tables based on your models


    @login_manager.user_loader
    def load_user(user_id: Any) -> (Any | None): # noqa
        return User.query.get(int(user_id))

    return app
