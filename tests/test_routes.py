from app.models.book import Book
from werkzeug.exceptions import HTTPException
from app.book_routes import validate_model
import pytest

def test_get_all_books_with_no_records(client):
    # ACT
    response = client.get("/books")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert response_body == []


def test_get_all_books_with_two_saved_books(client, two_saved_books):
    # ACT
    response = client.get("/books")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert len(response_body) == 2
    assert response_body[0] == {
        "id": 1,
        "title": "Twilight",
        "description": "Twilight Saga I"
    }
    assert response_body[1] == {
        "id": 2,
        "title": "New Moon",
        "description": "Twilight Saga II"
    }

def test_get_all_books_with_title_query_matching_none(client, four_saved_books):
    # ACT
    data = {"title": "Midnight Sun"}
    response = client.get("/books", query_string=data)
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert response_body == []

def test_get_all_books_with_title_query_matching_one(client, four_saved_books):
    # ACT
    data = {"title": "Breaking Dawn"}
    response = client.get("/books", query_string=data)
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert response_body[0] == { # does the [0] refer to the response_body and [1] refer to the status code?
        "id": 4,
        "title": "Breaking Dawn",
        "description": "Twilight Saga IV"
    }


def test_get_one_book(client, two_saved_books): # must add the two_saved_books fixture to the test's parameters. we can comma-separate as many fixutres as a single test needs
    # ACT
    response = client.get("/books/1")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert response_body == {
        "id": 1,
        "title": "Twilight",
        "description": "Twilight Saga I"
    }

def test_get_one_book_id_not_found(client, four_saved_books):
    # ACT
    response = client.get("/books/5")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 404
    assert response_body == {"message": "Book 5 not found"}

def test_get_one_book_id_invalid(client, four_saved_books):
    # ACT
    response = client.get("/books/blah")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 400
    assert response_body == {"message": "Book 'blah' is invalid"}


def test_create_one_book(client):
    # ACT
    response = client.post("/books", json={
        "title": "Midnight Sun",
        "description": "Twilight from Edward's perspective"
    })
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 201
    assert response_body == "Book Midnight Sun successfully created"

def test_create_one_book_no_title(client):
    # ARRANGE
    test_data = {
        "description": "Twilight from Edward's perspective"
    }

    # ACT / ASSERT
    with pytest.raises(KeyError, match="title"):
        response = client.post("/books", json=test_data)

def test_create_one_book_no_description(client):
    # ARRANGE
    test_data = {
        "title": "Midnight Sun"
    }

    # ACT / ASSERT
    with pytest.raises(KeyError, match="description"):
        response = client.post("/books", json=test_data)

def test_create_one_book_with_extra_keys(client, four_saved_books):
    # ARRANGE
    test_data = {
        "title": "Midnight Sun",
        "description": "Twilight from Edward's perspective",
        "author": "Stephenie Meyer"
    }

    # ACT
    response = client.post("/books", json=test_data)
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 201
    assert response_body == "Book Midnight Sun successfully created"


def test_update_book(client, two_saved_books):
    # ARRANGE
    test_data = {
        "title": "Twilight",
        "description": "the first Twilight book"
    } 

    # ACT
    response = client.put("/books/1", json=test_data)
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert response_body == "Book #1 successfully updated"

def test_update_book_with_extra_keys(client, two_saved_books):
    # ARRANGE
    test_data = {
        "title": "Twilight",
        "description": "the first Twilight book",
        "author": "Stephenie Meyer"
    } 

    # ACT
    response = client.put("/books/1", json=test_data)
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert response_body == "Book #1 successfully updated"

def test_update_book_with_missing_record(client, two_saved_books):
    # ARRANGE
    test_data = {
        "title": "Eclipse",
        "description": "Twilight Saga III"
    } 

    # ACT
    response = client.put("/books/3", json=test_data)
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

def test_update_book_with_missing_record(client, two_saved_books):
    # ARRANGE
    test_data = {
        "title": "Eclipse",
        "description": "Twilight Saga III"
    } 

    # ACT
    response = client.put("/books/blah", json=test_data)
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 400
    assert response_body == {"message": "Book 'blah' is invalid"}


def test_delete_book(client, two_saved_books):
    # ACT
    response = client.delete("/books/1")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 200
    assert response_body == "Book #1 successfully deleted"

def test_delete_book_with_missing_record(client, two_saved_books):
    # ACT
    response = client.delete("/books/3")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 404
    assert response_body == {"message": "Book 3 not found"}

# @pytest.mark.skip()
def test_delete_book_with_missing_record(client, two_saved_books):
    # ACT
    response = client.delete("/books/blah")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 400
    assert response_body == {"message": "Book 'blah' is invalid"}


def test_validate_model(two_saved_books):
    # ACT
    result_book = validate_model(Book, 1)

    # ASSERT
    assert result_book.id == 1
    assert result_book.title == "Twilight"
    assert result_book.description == "Twilight Saga I"

# @pytest.mark.skip()
def test_validate_model_missing_record(two_saved_books):
    # Calling validate_model without invoking a route will cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_model(Book, 3)

# @pytest.mark.skip()
def test_validate_model_invalid_id(two_saved_books):
    # Calling validate_model without invoking a route will cause an `HTTPException` when an `abort` statement is reached 
    with pytest.raises(HTTPException):
        result_book = validate_model(Book, "blah")