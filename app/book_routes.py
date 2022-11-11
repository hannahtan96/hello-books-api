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

# handle creation of new author instance if author do not currently exist
def return_author_from_name(author):
    chosen_author = Author.query.filter(Author.name==author).first()
    if chosen_author is None:
        new_author = Author.from_dict({"name":author})
        
        db.session.add(new_author)
        db.session.commit()
        return new_author
    else:
        return chosen_author


# handle creation of new genre instance(s) if any genre does not currently exist
def return_genres_from_genre_names(genre_names):
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

    return list_of_genres


@books_bp.route("", methods=["POST"])
def create_book():
    # use request object info on the http request
    # request.get_json() will "pythonify" the JSON HTTP request body by converting it into a Python dictionary
    request_body = request.get_json()
    
    try:
        author = return_author_from_name(request_body["author"])
        list_of_genres = return_genres_from_genre_names(request_body["genres"])

        new_book = Book(
            title=request_body["title"],
            description=request_body["description"],
            author=author,
            genres=list_of_genres
            )
        
        db.session.add(new_book)
        db.session.commit()
    except KeyError:
        return jsonify({"msg": "Missing book data"}), 400

    return jsonify(f"Book {new_book.title} by {new_book.author.name} successfully created"), 201


@books_bp.route("", methods=["GET"])
def read_all_books():
    # return make_response("I\'m a teapot!", 418)

    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response), 200


@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book, book_id)
    return jsonify(book.to_dict()), 200


@books_bp.route("/<book_id>", methods=["PUT", "PATCH"])
def update_book(book_id):
    book = validate_model(Book, book_id)

    request_body = request.get_json()
    if request_body["title"]:
        book.title = request_body["title"]
    if request_body["description"]:
        book.description = request_body["description"]
    if request_body["author"]:
        book.author = return_author_from_name(request_body["author"])
    if request_body["genres"]:
        book.genres = return_genres_from_genre_names(request_body["genres"])

    db.session.commit()
    return jsonify(f"Book #{book.id} successfully updated"), 204


@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return jsonify(f"Book #{book.id} successfully deleted"), 202




