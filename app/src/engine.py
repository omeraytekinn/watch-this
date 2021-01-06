from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from models import Movie


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


engine = create_engine('sqlite:///app/src/myblog.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

movies = session.query(Movie).filter(Movie.id < 5).all()

unwatched = session.query(Movie).filter(Movie.id >= 5).all()

watched = " ".join([combine_movie(i) for i in movies])

other_movies = [combine_movie(i) for i in unwatched]

matrix = create_cosine_matrix([watched, *other_movies])

similars = get_similars(matrix, 0, 10)

for i in similars:
    print(unwatched[i-1].title)
