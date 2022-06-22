from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///funnymovies.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    genre = db.Column(db.String(64), nullable=False)
    director = db.Column(db.String(128), nullable=False)
    rate = db.Column(db.Float, nullable=False)
    def toDict(self):
        return {
            'id': self.id,
            'title': self.title,
            'genre': self.genre,
            'director': self.director,
            'rate': self.rate
        }
    @staticmethod
    def new(movie_dict: dict) -> 'Movie':
        movie = Movie(
            title=movie_dict['title'],
            genre=movie_dict['genre'],
            director=movie_dict['director'],
            rate=movie_dict['rate']
        )
        db.session.add(movie)
        db.session.commit()
        return movie

@app.route('/movies', methods=['GET'])
def get_movies():
    ret = []
    for movie in Movie.query.all():
        ret.append(movie.toDict())
    return jsonify(ret)

@app.route('/movies/new', methods=['POST'])
def new_movie():
    try:
        movie_dict = request.get_json()
        Movie.new(movie_dict)
        return Response(status=201)
    except KeyError:
        return Response(status=400)
