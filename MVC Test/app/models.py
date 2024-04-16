# app/models.py
from . import db

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100))
    date = db.Column(db.String(50))
    filepath = db.Column(db.String(200))

    def __repr__(self):
        return f'<Document {self.title}>'
