import pytest
from app import create_app, db
from flask.signals import request_finished # @request.finished decorator creates a new db session after a request as described
from app.models.book import Book

@pytest.fixture
def app():
    app = create_app({"TESTING": True}) # create an app object, passing in a dictionary to represent a "test config"

    @request_finished.connect_via(app) # indicates that the function expire_session will be invoked after any request is completed
    def expire_session(sender, response, **extra):
        db.session.remove() # create new db session so we can test that changes wered persisted, mostly relevant for update method


    with app.app_context(): # makes sure the following code has an application context
        db.create_all() # recreates tables needed for models
        yield app # fixture suspends here, returning the app for use in tests and other fixtures


    with app.app_context():
        db.drop_all() # drop all tables, deleting any data that was created during the test


@pytest.fixture # set up a second fixture
def client(app): # fixture is called client, passing in app as a parameter
    return app.test_client() # responsible for making a test client, an object able to simulate a client making HTTP requests


@pytest.fixture # set up a third fixture that saves two books to a db
def two_saved_books(app):
    # ARRANGE
    twilight = Book(title="Twilight", description="Twilight Saga I")
    new_moon = Book(title="New Moon", description="Twilight Saga II")
    
    db.session.add_all([twilight, new_moon])
    db.session.commit()

@pytest.fixture # set up a fourth fixture that saves four books to a db
def four_saved_books(app):
    # ARRANGE
    twilight = Book(title="Twilight", description="Twilight Saga I")
    new_moon = Book(title="New Moon", description="Twilight Saga II")
    eclipse = Book(title="Eclipse", description="Twilight Saga III")
    breaking_dawn = Book(title="Breaking Dawn", description="Twilight Saga IV")

    db.session.add_all([twilight, new_moon, eclipse, breaking_dawn])
    db.session.commit()