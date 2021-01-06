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

def search_movie(name, page):
    return example_movies

def get_movies(page, sortby):
    return example_movies

def login(username, password):
    return True

def register(username, password):
    return username

def check_login(request):
    return False

def recommend_movies(user_id):
    return example_movies

def rate_movie(user_id, movie_id, score):
    return False