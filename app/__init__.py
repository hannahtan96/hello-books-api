from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    # hide warning about a feature in SQL that we won't be using
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    if not test_config:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI")
        
    else:
        app.config["TESTING"] = True
        # connection to db hello_books_development
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_TEST_DATABASE_URI")
    
    
    # connect db and migrate to flask
    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.book import Book
    from app.models.author import Author

    from .book_routes import books_bp
    app.register_blueprint(books_bp)

    from .book_routes import authors_bp
    app.register_blueprint(authors_bp)

    return app