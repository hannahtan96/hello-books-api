from turtle import title
from app import db
from app.models import book
from app.models.book import Book
from flask import Blueprint, make_response, request, jsonify, abort

books_bp = Blueprint("my_books_bp", __name__,url_prefix="/books")

# class Book:

#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book id \'{book_id}\' is invalid"}, 400))

    book = Book.query.get(book_id)
    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))
    else:
        return book


@books_bp.route("", methods=["POST"])
def create_book():
    # use request object info on the http request
    # request.get_json() will "pythonify" the JSON HTTP request body by converting it into a Python dictionary
    request_body = request.get_json()
    new_book = Book(
        title=request_body["title"],
        description=request_body["description"])
    
    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)


@books_bp.route("", methods=["GET"])
def read_all_books():
    # return make_response("I\'m a teapot!", 418)

    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append({
            "id": book.id,
            "title": book.title,
            "description": book.description
        })
    
    return jsonify(books_response) # why are we not using the make_response(jsonify(book_response), 200)


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id): # question: why don't we need to do the make_response({}, 200)
    book = validate_book(book_id)
    return {
            "id": book.id,
            "title": book.title,
            "description": book.description
            }


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()
    return make_response(jsonify(f"Book #{book.id} successfully updated"))


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))


