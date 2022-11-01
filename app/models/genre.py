from app import db

class Genre(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    # author_id = db.Column(db.Integer, db.ForeignKey('author.id'))

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    @classmethod
    def from_dict(cls, genre_data):
        new_genre = Genre(name=genre_data["name"])
        return new_genre