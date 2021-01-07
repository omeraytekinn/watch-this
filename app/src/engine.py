from sqlalchemy import create_engine, and_
from sqlalchemy.orm import sessionmaker
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
from .models import Movie, UserScore, User

engine = create_engine('sqlite:///app/src/myblog.db',
                       echo=False, connect_args={'check_same_thread': False})
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
    return " ".join([combine_movie(movie) for movie in movies])


def combine_list(movies):
    return [combine_movie(movie) for movie in movies]


def suggest_movie(liked_movies, unliked_movies, suggestion_number):
    liked_movies_ids = [i.id for i in liked_movies]
    unliked_movies_ids = [i.id for i in unliked_movies]

    unwatched_movies = session.query(Movie).filter(
        Movie.id.notin_([*liked_movies_ids, *unliked_movies_ids])).all()

    combined_liked_movies = combine_all(liked_movies)

    combined_unwatched_movies = combine_list(unwatched_movies)
    cosine_matrix = create_cosine_matrix(
        [combined_liked_movies, *combined_unwatched_movies])
    suggesteds = get_similars(cosine_matrix, 0, suggestion_number)

    return [unwatched_movies[i-1].id for i in suggesteds]


def recommend_movie(user_id):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    likeds = [i.movie for i in session.query(UserScore).filter(
        and_(UserScore.user_id == user_id, UserScore.score > 6)).all()]
    unlikeds = [i.movie for i in session.query(UserScore).filter(
        and_(UserScore.user_id == user_id, UserScore.score <= 6)).all()]

    suggesteds = suggest_movie(likeds, unlikeds, 4)
    
    return [session.query(Movie).filter(Movie.id == i).first() for i in suggesteds]


if __name__ == "__main__":
    print(recommend_movies()[0])
