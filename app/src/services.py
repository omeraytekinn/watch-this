import jwt
import datetime
from .engine import recommend_movie
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from .models import User, Movie, UserScore
from werkzeug.security import check_password_hash, generate_password_hash

engine = create_engine('sqlite:///app/src/myblog.db',
                       echo=False, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
session = Session()

SECRET_KEY = "secret"


def search_movie(name, page):
    print(name)
    movies = session.query(Movie).filter(Movie.title.contains(name)).all()
    movies = movies_to_dict(movies[5*(page-1):5*(page)])
    return movies


def movies_to_dict(movies):
    titles = [i.title for i in movies]
    years = [i.year for i in movies]
    posters = [i.poster for i in movies]
    genres = [[g.name for g in i.genres] for i in movies]
    imdb_ratings = [i.imdb_rating for i in movies]
    casts = [[c.name for c in i.actors] for i in movies]
    directors = [i.director.name for i in movies]
    temp = dict()
    for i, movie in enumerate(movies):
        temp[movie.id] = {'title': titles[i],
                          'year': years[i],
                          'poster': posters[i],
                          'genre': genres[i],
                          'imdb_rating': imdb_ratings[i],
                          'cast': casts[i],
                          'director': directors[i]
                          }
    return temp


def get_movies(page, sortby, asc=False):
    if asc:
        s = asc
    else:
        s = desc
    sorts = [
        "title",
        "year",
        "duration",
        "imdb_rating",
    ]
    list_count = 4
    if sortby not in sorts:
        return False
    movies = session.query(Movie).order_by(
        s(sortby)).all()[list_count*(page-1):list_count*(page)]
    movies = movies_to_dict(movies)
    return movies


def login(username, password):
    user = session.query(User).filter(User.username == username).first()
    if user and check_password_hash(user.password, password):
        token = create_token(username)
        return token
    return False


def register(name, username, email, password):
    user = session.query(User).filter_by(username=username).first()
    user2 = session.query(User).filter_by(email=email).first()
    if user:
        return 1
    if user2:
        return 2
    hashed = generate_password_hash(password)
    user = User(name=name, username=username, email=email, password=hashed)
    session.add(user)
    session.commit()
    return True


def check_login(token):
    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = decoded['username']
        expiration_time = datetime.datetime.fromtimestamp(decoded['exp'])
    except:
        return None
    user = session.query(User).filter(User.username == username).first()
    if not user:
        return None
    if datetime.datetime.now() > expiration_time:
        return None
    return user


def recommend_movies(user_id):
    recommendeds = recommend_movie(user_id)
    recommendeds = movies_to_dict(recommendeds)
    return recommendeds


def rate_movie(user_id, movie_id, score):
    user = session.query(User).filter_by(id=user_id).first()
    movie = session.query(Movie).filter_by(id=movie_id).first()
    if not user or not movie:
        return False
    user_score = session.query(UserScore).filter_by(
        user_id=user_id, movie_id=movie_id).first()
    if user_score:
        user_score.score = score
    else:
        user_score = UserScore(movie=movie, user=user, score=score)
    session.add(user_score)
    session.commit()
    return True


def create_token(username):
    expiration_time = datetime.datetime.now() + datetime.timedelta(days=1)
    token = jwt.encode({"username": username, "exp": expiration_time.timestamp(
    )}, SECRET_KEY, algorithm="HS256")
    return token
