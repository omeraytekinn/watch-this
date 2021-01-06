example_movies = {
    "1": {
    "name": "The Shawshank Redemption",
    "year": 1994,
    "img": "https://m.media-amazon.com/images/M/MV5BMDFkYTc0MGEtZmNhMC00ZDIzLWFmNTEtODM1ZmRlYWMwMWFmXkEyXkFqcGdeQXVyMTMxODk2OTU@._V1_UX512.jpg",
    "genre": "Drama",
    "rate": 9.3,
    "rating_count": 2329254
    },
    "2": {
    "name": "The Godfather",
    "year": 1972,
    "img": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UY512.jpg",
    "genre": "Crime, Drama ",
    "rate": 9.2,
    "rating_count": 1609628
    },
    "3": {
    "name": "The Lord of the Rings: The Return of the King",
    "year": 2003,
    "img": "https://m.media-amazon.com/images/M/MV5BNzA5ZDNlZWMtM2NhNS00NDJjLTk4NDItYTRmY2EwMWZlMTY3XkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_UX512.jpg",
    "genre": "Action, Adventure, Drama",
    "rate": 8.9,
    "rating_count": 1634781
    },
    "4": {
    "name": "The Dark Knight",
    "year": 2006,
    "img": "https://m.media-amazon.com/images/M/MV5BMTIzMDc4MzA2Ml5BMl5BanBnXkFtZTcwODU0MzA3MQ@@._V1_FMjpg_UX510_.jpg",
    "genre": "Action, Crime, Drama",
    "rate": 9.0,
    "rating_count": 2290938
}}

def search_movie(name, page):
    return example_movies

def get_movies(page, sortby):
    return example_movies

def login(username, password):
    return True

def register(username, password):
    return username

def check_login():
    return False

def recommend_movies():
    return example_movies

def rate_movie(id, score):
    return False