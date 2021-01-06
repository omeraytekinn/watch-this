from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from models import Movie

engine = create_engine('sqlite:///app/src/myblog.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def create_cosine_matrix(arr):
    cm = CountVectorizer().fit_transform(arr)
    cs = cosine_similarity(cm)
    return cs


def get_similars(cosine_matrix, origin_row_num, similar_count):
    scores = {i: s for i, s in enumerate(
        cosine_matrix[origin_row_num]) if origin_row_num != i}
    scores = scores.items()
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    similars = [i[0] for i in scores[:similar_count]]
    return similars


def combine_movie(movie):
    actors = [actor.name for actor in movie.actors]
    genres = [genres.name for genres in movie.genres]
    title = movie.title
    director = movie.director.name
    return " ".join([title, director, *actors, *genres])


def combine_all(movies):
    watched_movies = " ".join([combine_movie(movie) for movie in movies])
    return watched_movies


def combine_list(movies):
    return [combine_movie(movie) for movie in movies]


def suggest_movie(watched_movies, suggestion_number):
    watched_movies_ids = [i.id for i in watched_movies]
    unwatched_movies = session.query(Movie).filter(
        Movie.id.notin_(watched_movies_ids)).all()
    combined_watched_movies = combine_all(watched_movies)
    combined_unwatched_movies = combine_list(unwatched_movies)
    cosine_matrix = create_cosine_matrix(
        [combined_watched_movies, *combined_unwatched_movies])
    suggesteds = get_similars(cosine_matrix, 0, suggestion_number)
    return [unwatched_movies[i-1].id for i in suggesteds]


gf1 = session.query(Movie).filter(Movie.id == 2).first()
gf2 = session.query(Movie).filter(Movie.id == 4).first()

suggesteds = suggest_movie([gf1, gf2], 10)

for i in suggesteds:
    print(session.query(Movie).filter(Movie.id == i).first().title)
