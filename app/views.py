from typing import ContextManager
from flask.globals import session
from jinja2.utils import contextfunction
from flask import Flask, render_template, redirect, Response, request, make_response
from .src import services

app = Flask(__name__)


@app.context_processor
def inject_user():
    token = request.cookies.get("token")
    auth_username = services.check_login(token)
    is_login = False
    if auth_username:
        is_login = True
        return dict(is_login=is_login, username=auth_username)
    return dict(is_login=is_login)


@app.route('/')
def index():
    token = request.cookies.get("token")
    username = services.check_login(token)
    recommended_movies = None
    if username:
        pass
        #recommended_movies = services.recommend_movies(username)
    top_movies = services.get_movies(1, "rate")
    return render_template("index.html", recommended_movies=recommended_movies, top_movies=top_movies)


@app.route('/rate-movie/<id>/<score>')
def rate(id, score):
    token = request.cookies.get("token")
    username = services.check_login(token)
    result = None
    if username:
        result = services.rate_movie(username, id, score)
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
    movies = services.get_movies(page, "imdb_rating")
    return render_template("movies.html", movies=movies)


@app.route('/movies/search/<name>')
def search_movies(name):
    return redirect("/search/" + name + "/1", 302)


@app.route('/movies/search/<name>/<page>')
def search_movies_paged(name, page):
    return render_template("movies.html")


@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    jwt = services.login(username, password)
    if jwt:
        resp = make_response(redirect("/", 302))
        resp.set_cookie("token", jwt)
        return resp
    resp = make_response(redirect("/", 401))
    return resp


@app.route('/logout')
def logout():
    token = request.cookies.get("token")
    resp = make_response(redirect("/", 302))
    if token:
        resp.delete_cookie("token")
    return resp


@app.route('/error')
def error():
    return "Hatalı işlem"


@app.route('/register', methods=['POST'])
def register():
    name = request.form['name']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    r = services.register(name, username, email, password)
    if r == 1 or r == 2:
        resp = make_response(redirect("/", 302))
        return resp
    resp = make_response(redirect("/", 302))
    return resp
