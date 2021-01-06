from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Movie, Actor, Director, Genre, create_db
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
engine = create_engine('sqlite:///myblog.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()


def create_cosine_matrix(arr):
    cm = CountVectorizer().fit_transform(arr)
    cs = cosine_similarity(cm)
    return cs


def get_similars(cosine_matrix, row, num):
    scores = {i: s for i, s in enumerate(cosine_matrix[row]) if row != i}
    scores = scores.items()
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    similars = [i[0] for i in scores[:num]]
    return similars


df = pd.read_csv("movies.csv")

df = df[["title", "year", "duration", "genre", "imdb_rating", "director", "cast"]]
