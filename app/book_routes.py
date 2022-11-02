from app import db
from app.models.book import Book
from app.models.author import Author
from app.models.genre import Genre
from flask import abort, Blueprint, jsonify, make_response, request

books_bp = Blueprint("books_bp", __name__,url_prefix="/books")


def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message": f"{cls.__name__} \'{model_id}\' is invalid"}, 400))

    model = cls.query.get(model_id)
    if not model:
        abort(make_response({"message": f"{cls.__name__} {model_id} not found"}, 404))
    return model


@books_bp.route("", methods=["POST"])
def create_book():
    # use request object info on the http request
    # request.get_json() will "pythonify" the JSON HTTP request body by converting it into a Python dictionary
    request_body = request.get_json()
    author_name = request_body["author"]

    # handle creation of new author instance if author do not currently exist
    chosen_author = Author.query.filter(Author.name==author_name).first()
    if chosen_author is None:
        new_author = Author.from_dict({"name":author_name})
        
        db.session.add(new_author)
        db.session.commit()
        
        output_author = new_author

    else:
        output_author = chosen_author

    # handle creation of new genre instance(s) if any genre does not currently exist
    genre_names = request_body["genres"]
    list_of_genres = []
    for genre_name in genre_names:
        chosen_genre = Genre.query.filter(Genre.name==genre_name).first()
        if chosen_genre is None:
            new_genre = Genre.from_dict({"name":genre_name})

            db.session.add(new_genre)
            db.session.commit()

            list_of_genres.append(new_genre)
            
        else:
            list_of_genres.append(chosen_genre)

    output_genres = list_of_genres

    new_book = Book(
        title=request_body["title"],
        description=request_body["description"],
        author=output_author,
        genres=output_genres
        )
    
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

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response) # why are we not using the make_response(jsonify(book_response), 200)


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id): # question: why don't we need to do the make_response({}, 200)
    book = validate_model(Book, book_id)
    return book.to_dict()


@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_model(Book, book_id)

    request_body = request.get_json()
    book.title = request_body["title"]
    book.description = request_body["description"]
    book.author = request_body["author"]
    book.genres = request_body["genres"]

    db.session.commit()
    return make_response(jsonify(f"Book #{book.id} successfully updated"))


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"))




