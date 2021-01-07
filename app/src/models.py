from sqlalchemy import Column, Integer, String, Float, create_engine, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()


movie_actor_link = Table(
    'movie_actor_link',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('actor_id', Integer, ForeignKey('actors.id'), primary_key=True),
)

movie_genre_link = Table(
    'movie_genre_link',
    Base.metadata,
    Column('movie_id', Integer, ForeignKey('movies.id'), primary_key=True),
    Column('genre_id', Integer, ForeignKey('genres.id'), primary_key=True),
)


class Movie(Base):
    __tablename__ = 'movies'
    id = Column(Integer, primary_key=True)
    title = Column(String)
    year = Column(Integer)
    poster = Column(String)
    duration = Column(Integer)
    imdb_rating = Column(Float)
    metascore_rating = Column(Float)
    director = relationship("Director", back_populates="movies")
    director_id = Column(Integer, ForeignKey('directors.id'))
    actors = relationship(
        "Actor", secondary=movie_actor_link, back_populates="movies")
    genres = relationship(
        "Genre", secondary=movie_genre_link, back_populates="movies")
    scores = relationship("UserScore", back_populates="movie")

    def __repr__(self):
        return "<Movie(title='%s', year='%s', imdb_rating='%s')>" % (
            self.title, self.year, self.imdb_rating)


class Director(Base):
    __tablename__ = 'directors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship("Movie", back_populates="director")

    def __repr__(self):
        return "<Director(name='%s')>" % (self.name)


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship(
        "Movie", secondary=movie_actor_link, back_populates="actors")

    def __repr__(self):
        return "<Actor(name='%s')>" % (self.name)


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship(
        "Movie", secondary=movie_genre_link, back_populates="genres")

    def __repr__(self):
        return "<Genre(name='%s')>" % (self.name)


class UserScore(Base):
    __tablename__ = 'user_score'
    id = Column(Integer, primary_key=True)
    score = Column(Integer)
    user = relationship("User", back_populates="scores")
    user_id = Column(Integer, ForeignKey('users.id'))
    movie = relationship("Movie", back_populates="scores")
    movie_id = Column(Integer, ForeignKey('movies.id'))

    def __repr__(self):
        return "<UserScore(user_name='%s', movie_name='%s', user_score='%s')>" % (
            self.user.name, self.movie.name, self.score)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    username = Column(String, nullable=False, unique=True)
    email = Column(String, nullable=False, unique=True)
    scores = relationship("UserScore", back_populates="user")
    password = Column(String, nullable=False)

    def __repr__(self):
        return "<User(email='%s')>" % (self.name)


def create_db():
    engine = create_engine(
        "sqlite:///myblog.db?check_same_thread=False", echo=False, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
