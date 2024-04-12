from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()
DB_NAME="Historical_Database.db"

def create_app():
    HistoricApp = Flask(__name__)
    HistoricApp.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' 
    
    HistoricApp.config['SECRET_KEY'] = 'secretkey'
    
    db.init_app(HistoricApp)
     
    @HistoricApp.route('/')
    def home():
        return render_template("index.html")




if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
