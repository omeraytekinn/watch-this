from flask import Flask, render_template, redirect, Response, request, make_response
from .src import services
import math
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
app = Flask(__name__)


engine = create_engine('sqlite:///app/src/myblog.db',
                       echo=False, connect_args={'check_same_thread': False})
Session = sessionmaker(bind=engine)
session = Session()


@app.context_processor
def inject_user():
    token = request.cookies.get("token")
    user = services.check_login(token)
    is_login = False
    if user:
        is_login = True
        return dict(is_login=is_login, username=user.name)
    return dict(is_login=is_login)


@app.route('/')
def index():
    token = request.cookies.get("token")
    user = services.check_login(token)
    recommended_movies = None
    is_login = False
    if user:
        is_login = True
        recommended_movies = services.recommend_movies(user.id)
    top_movies, length = services.get_movies(1, "imdb_rating", 4)
    return render_template("index.html", is_login=is_login, recommended_movies=recommended_movies, top_movies=top_movies)

    
 

@app.route('/rate-movie/<movie_id>/<score>')
def rate(movie_id, score):
    token = request.cookies.get("token")
    user = services.check_login(token)
    result = None
    if user:
        result = services.rate_movie(user.id, movie_id, score)
        if result:
            return Response(status=200, mimetype='application/json')
    return Response(status=400, mimetype='application/json')


@app.route('/movies')
def movies():
    return redirect("/movies/all/1", 302)


@app.route('/movies/all/<page>')
def all_movies(page):
    movies, total_movies = services.get_movies(int(page), "imdb_rating", 5)
    token = request.cookies.get("token")
    user = services.check_login(token)
    if user:
        scores = user.scores
        keys = movies.keys()
        for i in scores:
            if i.movie_id in keys:
                movies[i.movie_id]["user_score"] = i.score
    total_page = math.ceil(total_movies/5)
    return render_template("movies.html", movies=movies, page=page, total_page=total_page, total_movies=total_movies)



@app.route('/movies/search/<name>')
def search_movies(name):
    return redirect("/movies/search/" + name + "/1", 302)


@app.route('/movies/search/<name>/<page>')
def search_movies_paged(name, page):
    movies, total_movies = services.search_movie(name, int(page))
    token = request.cookies.get("token")
    user = services.check_login(token)
    if user:
        scores = user.scores
        keys = movies.keys()
        for i in scores:
            if i.movie_id in keys:
                movies[i.movie_id]["user_score"] = i.score
    total_page = math.ceil(total_movies/5)
    return render_template("movies.html", movies=movies, page=page, total_page=total_page, total_movies=total_movies)


@app.route('/login', methods=["POST"])
def login():
    username = request.form['username']
    password = request.form['password']
    jwt = services.login(username, password)
    if jwt:
        resp = make_response(redirect("/", 302))
        resp.set_cookie("token", jwt)
        return resp
    resp = make_response(redirect("/", 302))
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
