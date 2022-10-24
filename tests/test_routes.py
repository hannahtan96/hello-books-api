
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
    assert response_body == {"message": "book 5 not found"}


def test_get_one_book_id_invalid(client, four_saved_books):
    # ACT
    response = client.get("/books/blah")
    response_body = response.get_json()

    # ASSERT
    assert response.status_code == 400
    assert response_body == {"message": "book id 'blah' is invalid"}


def test_create_one_book(client):
    # ACT
    response = client.post("/books", json={
        "title": "Midnight Sun",
        "description": "Twilight from Edward's perspective"
    })
    response_body = response.get_json()
    print(response_body)

    # ASSERT
    assert response.status_code == 201
    assert response_body == "Book Midnight Sun successfully created"