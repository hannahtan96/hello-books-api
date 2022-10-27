from app.models.book import Book
import pytest

def test_to_dict_no_missing_data():
    # ARRANGE
    test_data = Book(id=1, title="Twilight", description="Twilight Saga I")

    # ACT
    result = test_data.to_dict()

    # ASSERT
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Twilight"
    assert result["description"] == "Twilight Saga I"


def test_to_dict_missing_id():
    # ARRANGE
    test_data = Book(title="Twilight", description="Twilight Saga I")

    # ACT
    result = test_data.to_dict()

    # ASSERT
    assert len(result) == 3
    assert result["id"] is None
    assert result["title"] == "Twilight"
    assert result["description"] == "Twilight Saga I"


def test_to_dict_missing_title():
    # ARRANGE
    test_data = Book(id=1, description="Twilight Saga I")

    # ACT
    result = test_data.to_dict()

    # ASSERT
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] is None
    assert result["description"] == "Twilight Saga I"


def test_to_dict_missing_description():
    # ARRANGE
    test_data = Book(id=1, title="Twilight")

    # ACT
    result = test_data.to_dict()

    # ASSERT
    assert len(result) == 3
    assert result["id"] == 1
    assert result["title"] == "Twilight"
    assert result["description"] is None


def test_from_dict_returns_book():
    # ARRANGE
    book_data = {
        "title": "Midnight Sun",
        "description": "Twilight from Edward's perspective"
    }

    # ACT
    new_book = Book.from_dict(book_data)

    # ASSERT
    assert new_book.title == "Midnight Sun"
    assert new_book.description == "Twilight from Edward's perspective"