from flask.globals import session
from app import app
from flask import render_template, redirect, Response, request
import app.src.services as services


@app.route('/')
def index():
    jwt = request.headers.get("jwt")
    user = services.check_login(jwt)
    is_login = False
    recommended_movies = None
    if user:
        recommended_movies = services.recommend_movies(user.name)
        
    top_movies = services.get_movies(1, "rate")
    return render_template("index.html", is_login=is_login, recommended_movies=recommended_movies, top_movies=top_movies)

@app.route('/rate-movie/<id>/<score>')
def rate(id, score):
    result = services.rate_movie(id, score)
    if result:
        return Response("Successful!", status=200, mimetype='application/json')
    else:
        return Response("Unknown Error!", status=400, mimetype='application/json')
    

@app.route('/movies')
def movies():
    return redirect("/movies/all/1", 302)

@app.route('/movies/all/<page>')
def all_movies(page):
    # TODO: Burada page numarasına göre sıradaki filmler çekilecek
    # movies = [{...},{...},...] yapısında bir değişkene konulacak
    return render_template("movies.html", movies=popular_movies)
@app.route('/movies/search/<name>')
def search_movies(name):
    return redirect("/search/" + name + "/1", 302)

@app.route('/movies/search/<name>/<page>')
def search_movies_paged(name, page):
    return render_template("movies.html")

@app.route('/login', methods=["POST"])
def login():
    # TODO: Buraya giriş işlemleri gelecek sonuç başarılıysa anasayfaya yönlendirecek
    username = request.form['username']
    password = request.form['password']
    jwt = services.login(username, password)
    if jwt:
        return redirect("/", 302)
    else:
        return redirect("/error", 302)

@app.route('/error')
def error():
    return "Hatalı işlem"