from app import db

class Book(db.Model): # book inherits from db.Model from SQLAlchemy
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String)
    description = db.Column(db.String)