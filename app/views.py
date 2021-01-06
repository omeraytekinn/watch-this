from flask.globals import session
from app import app
from flask import render_template, redirect

popular_movies = {
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

@app.route('/')
def index():
    return render_template("index.html", popular_movies=popular_movies)

@app.route('/movies')
def movies():
    return redirect("/movies/all/1", 302)

@app.route('/movies/all/<page>')
def all_movies(page):
    # TODO: Burada page numarasına göre sıradaki filmler çekilecek
    # movies = [{...},{...},...] yapısında bir değişkene konulacak
    return render_template("movies.html", movies=popular_movies)
@app.route('/movies/search/')
def search_movies():
    return render_template("movies.html")

@app.route('/login')
def login():
    # TODO: Buraya giriş işlemleri gelecek sonuç başarılıysa anasayfaya yönlendirecek
    return redirect("/",302)
