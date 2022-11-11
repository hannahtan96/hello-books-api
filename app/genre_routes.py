from app import db
from app.models.book import Book
from app.models.genre import Genre
from app.models.book_genre import BookGenre
from app.book_routes import validate_model, return_author_from_name
from flask import abort, Blueprint, jsonify, make_response, request

genres_bp = Blueprint("genres_bp", __name__,url_prefix="/genres")

@genres_bp.route("", methods=["POST"])
def create_genre():

    request_body = request.get_json()
    new_genre = Genre.from_dict(request_body)
    
    db.session.add(new_genre)
    db.session.commit()

    return make_response(jsonify(f"Genre {new_genre.name} successfully created"), 201)


@genres_bp.route("", methods=["GET"])
def get_all_genres():
    genre_query = request.args.get("name")
    if genre_query:
        genres = Genre.query.filter_by(name=genre_query)
    else:
        genres = Genre.query.all()

    genres_response = [genre.to_dict() for genre in genres]
    return jsonify(genres_response), 200


@genres_bp.route("/<genre_id>/books", methods=["POST"])
def create_book(genre_id):
    chosen_genre = validate_model(Genre, genre_id)

    request_body = request.get_json()

    try:
        new_book = Book(
            title = request_body["title"],
            description = request_body["description"],
            author = return_author_from_name(request_body["author"]),
            genres=[chosen_genre]
        )

        db.session.add(new_book)
        db.session.commit()
    except KeyError:
        return jsonify({"msg": "Missing book data"}), 400

    return jsonify({"msg": f"Book {new_book.title} by {new_book.author.name} successfully created"}), 201


@genres_bp.route("/<genre_id>", methods=["GET"])
def get_one_genre(genre_id): # question: why don't we need to do the make_response({}, 200)
    genre = validate_model(Genre, genre_id)
    return genre.to_dict()
    

@genres_bp.route("/<genre_id>/books", methods=["GET"])
def read_all_books(genre_id):
    genre = validate_model(Genre, genre_id)
    books = Book.query.filter(Book.genres.contains(genre))

    books_response = [book.to_dict() for book in books]
    return jsonify(books_response), 200


@genres_bp.route("/<genre_id>", methods=["DELETE"])
def delete_genre(genre_id):
    genre = validate_model(Book, genre_id)

    db.session.delete(genre)
    db.session.commit()

    return mjsonify(f"Genre #{genre.id} successfully deleted"), 202