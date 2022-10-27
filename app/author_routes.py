from app import db
from app.book_routes import validate_model
from app.models.book import Book
from app.models.author import Author
from flask import Blueprint, make_response, request, jsonify, abort

authors_bp = Blueprint("authors_bp", __name__,url_prefix="/authors")

@authors_bp.route("", methods=["POST"])
def create_author():

    request_body = request.get_json()
    new_author = Author.from_dict(request_body)
    
    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)


@authors_bp.route("", methods=["GET"])
def read_all_authors():

    author_query = request.args.get("author")
    if author_query:
        authors = Author.query.filter_by(title=author_query)
    else:
        authors = Author.query.all()

    authors_response = []
    for author in authors:
        authors_response.append(author.to_dict())
    
    return jsonify(authors_response)


@authors_bp.route("/<author_id>/books", methods=["POST"])
def create_book(author_id):

    author = validate_model(Author, author_id)

    request_body = request.get_json()
    new_book = Book(
        title = request_body["title"],
        description = request_body["description"],
        author = author
    )

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201)


@authors_bp.route("/<author_id>/books", methods=["GET"])
def read_all_books(author_id):

    author = validate_model(Author, author_id)
    books = Book.query.filter_by(author=author)

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    
    return jsonify(books_response)