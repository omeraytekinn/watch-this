from requests import get
from bs4 import BeautifulSoup
import csv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pandas as pd
from .models import Movie, Actor, Director, Genre, create_db
import os
import re


def get_movies():
    csv_file = open("movies.csv", "w")
    # initialize csv headers
    fieldnames = ['title', 'year', 'poster', 'duration', 'genre',
                  'imdb_rating', 'metascore_rating', 'director', 'cast']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    # scrape page 1-20
    for page in range(20):
        url = "https://www.imdb.com/search/title/?groups=top_1000&view=advanced&sort=user_rating,desc&start=" + \
            str(page*50)
        response = get(url)
        # create BeautifulSoup object
        html_soup = BeautifulSoup(response.text, 'html.parser')
        # extract 50 movie containers
        movie_containers = html_soup.find_all(
            'div', class_='lister-item mode-advanced')
        for container in movie_containers:
            header = container.find('h3', class_='lister-item-header')
            title = header.a.text.strip()
            poster = container.find('div', class_='lister-item-image float-left').a.img['loadlate'].rsplit(
                '@', 1)[0]+"@._V1_UX546_CR0,0,546,804_AL_.jpg"
            year_temp = container.find(
                'span', class_="lister-item-year text-muted unbold").text
            year = re.findall(r"\(([0-9]{4})\)", year_temp)[0]
            duration = container.find(
                'span', class_='runtime').text[:-3].strip()
            genre = container.find('span', class_='genre').text.strip()
            imdb_rating = container.find(
                'div', class_='ratings-bar').find('strong').text.strip()
            try:
                metascore_rating = container.find(
                    'div', class_='inline-block ratings-metascore').span.text.strip()
            except:
                metascore_rating = 0
            people = container.find('p', class_='').find_all('a')
            director = people[0].text.strip()
            cast = ", ".join([i.text.strip() for i in people[1:]])
            writer.writerow({'title': title, 'year': year, 'poster': poster, 'duration': duration, 'genre': genre,
                             'imdb_rating': imdb_rating, 'metascore_rating': metascore_rating, 'director': director, 'cast': cast})
    csv_file.close()


def save_to_db():
    create_db()
    print("movies fetching")
    get_movies()
    print("db creating")
    engine = create_engine('sqlite:///myblog.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    df = pd.read_csv("movies.csv")
    for i in range(len(df)):
        m = session.query(Movie).filter_by(
            title=df.iloc[i]['title'], year=int(df.iloc[i]['year']))
        if m:
            pass

        movie = Movie(title=df.iloc[i]['title'], year=int(df.iloc[i]['year']), poster=df.iloc[i]['poster'], duration=int(
            df.iloc[i]['duration']), imdb_rating=df.iloc[i]['imdb_rating'], metascore_rating=df.iloc[i]['metascore_rating'])
        session.add(movie)

        director = session.query(Director).filter_by(
            name=df.iloc[i]['director']).first()
        if not director:
            director = Director(name=df.iloc[i]['director'])
            session.add(director)
        director.movies.append(movie)

        genres = df.iloc[i]["genre"].split(",")
        for genre in genres:
            g = session.query(Genre).filter_by(name=genre).first()
            if not g:
                g = Genre(name=genre)
                session.add(g)
            movie.genres.append(g)

        actors = df.iloc[i]['cast'].split(",")
        for actor in actors:
            a = session.query(Actor).filter_by(name=actor).first()
            if not a:
                a = Actor(name=actor)
                session.add(a)
            movie.actors.append(a)

        session.commit()


if __name__ == "__main__":

    save_to_db()
