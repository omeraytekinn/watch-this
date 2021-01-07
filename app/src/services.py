import jwt
import datetime
from .engine import recommend_movie
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import User
from werkzeug.security import check_password_hash, generate_password_hash


engine = create_engine('sqlite:///app/src/myblog.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

example_movies = {
    "1": {
        "title": "The Shawshank Redemption",
        "year": 1994,
        "poster": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX512.jpg",
        "genre": "Drama",
        "imdb_rating": 9.3,
        "cast": [],
        "director": "",
    },
    "2": {
        "title": "The Godfather",
        "year": 1972,
        "poster": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY512.jpg",
        "genre": ["Crime", "Drama"],
        "imdb_rating": 9.3,
        "cast": [],
        "director": "",
    },
    "3": {
        "title": "The Lord of the Rings: The Return of the King",
        "year": 2003,
        "poster": "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWZlMTY3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UX512.jpg",
        "genre": ["Crime", "Drama"],
        "imdb_rating": 9.3,
        "cast": [],
        "director": ""
    },
    "4": {
        "title": "The Dark Knight",
        "year": 2006,
        "poster": "https://m.media-amazon.com/images/M/MV5BMTIzMDc4MzA2Ml5BMl5BanBnXkFtZTcwODU0MzA3MQ@@._V1_FMjpg_UX510_.jpg",
        "genre": ["Crime", "Drama"],
        "imdb_rating": 9.3,
        "cast": [],
        "director": ""
    }}
SECRET_KEY = "secret"


def search_movie(name, page):
    return example_movies


def get_movies(page, sortby):
    return example_movies


def login(username, password):
    user = session.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        token = create_token(username)
        return token
    return False


def register(username, password):
    # TODO: veritabanı işlemleri
    token = create_token(username)
    return token


def check_login(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = decoded['username']
        expiration_time = datetime.datetime.fromtimestamp(decoded['exp'])
    except:
        return False
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return False
    now = datetime.datetime.now()
    if datetime.datetime.now() > expiration_time:
        return False
    return user


def recommend_movies(user_id):
    recommendeds = recommend_movie()
    titles = [i.title for i in recommendeds]
    years = [i.year for i in recommendeds]
    posters = [i.poster for i in recommendeds]
    genres = [[g.name for g in i.genres] for i in recommendeds]
    imdb_ratings = [i.imdb_rating for i in recommendeds]
    casts = [[c.name for c in i.actors] for i in recommendeds]
    directors = [i.director.name for i in recommendeds]
    temp = dict()
    for i, movie in enumerate(recommendeds):
        temp[movie.id] = {"title": titles[i],
                          "year": years[i],
                          "poster": posters[i],
                          "genre": genres[i],
                          "imdb_rating": imdb_ratings[i],
                          "cast": casts[i],
                          "director": directors[i]
                          }
    return temp


def rate_movie(user_id, movie_id, score):
    return True


def create_token(username):
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
    token = jwt.encode({"username": username, "exp": expiration_time.timestamp(
    )}, SECRET_KEY, algorithm="HS256")
    return token
