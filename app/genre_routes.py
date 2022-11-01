import json
from app import db
from app.models.book import Book
from app.models.genre import Genre
from app.book_routes import validate_model
from flask import Blueprint, make_response, request, jsonify, abort

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

    genres_response = []
    for genre in genres:
        genres_response.append(genre.to_dict())
    
    return jsonify(genres_response), 200


@genres_bp.route("/<genre_id>/books", methods=["POST"])
def create_book(genre_id):
    chosen_genre = validate_model(Genre, genre_id)

    request_body = request.get_json()
    new_book = Book(
        title = request_body["title"],
        description = request_body["description"],
        author_id = request_body["author_id"],
        genres=[chosen_genre]
    )

    db.session.add(new_book)
    db.session.commit()
    return jsonify({"msg": f"Book {new_book.title} by {new_book.author.name} successfully created"}), 201


@genres_bp.route("/<genre_id>", methods=["GET"])
def get_one_genre(genre_id): # question: why don't we need to do the make_response({}, 200)
    genre = validate_model(Genre, genre_id)
    return genre.to_dict()
    

@genres_bp.route("/<genre_id>/books", methods=["GET"])
def read_all_books(genre_id):
    genre = validate_model(Genre, genre_id)

    books_response = []
    for book in genre.books:
        books_response.append(book.to_dict())

    return jsonify(books_response), 200


@genres_bp.route("/<genre_id>", methods=["DELETE"])
def delete_genre(genre_id):
    genre = validate_model(Book, genre_id)

    db.session.delete(genre)
    db.session.commit()

    return make_response(jsonify(f"Genre #{genre.id} successfully deleted"))