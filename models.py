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

    def __repr__(self):
        return "<User(title='%s', year='%s', imdb_rating='%s')>" % (
            self.title, self.year, self.imdb_rating)


class Director(Base):
    __tablename__ = 'directors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship("Movie", back_populates="director")


class Actor(Base):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship(
        "Movie", secondary=movie_actor_link, back_populates="actors")


class Genre(Base):
    __tablename__ = 'genres'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    movies = relationship(
        "Movie", secondary=movie_genre_link, back_populates="genres")


def create_db():
    engine = create_engine(
        "sqlite:///myblog.db?check_same_thread=False", echo=False)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_db()
