import json
import os
import urllib.error
import urllib.parse
import urllib.request


def getMovies(movie, db, language):
    if not db:
        db = "all"
    if db.lower() == "tmdb":
        print("[!] Searching on tmdb")
        movies = getTMDB(movie, language)
    elif db.lower() == "omdb":
        print("[!] Searching on omdb")
        movies = getOMDB(movie)
    elif db.lower() == "all":
        print("[!] Searching on tmdb")
        movies = getTMDB(movie, language)
        if not movies:
            print("[!] Searching on omdb")
            movies = getOMDB(movie)
    return movies


def manualSearch(usermovie, language):
    movies = getTMDB(usermovie, language)
    if not movies:
        movies = getOMDB(usermovie)
    if not movies:
        return
    return movies


def getTMDB(movie, language):
    try:
        if not language:
            language = "en-US"
        movie_web = os.path.splitext(movie)[0]
        request_url = "https://api.themoviedb.org/3/search/movie" + \
            "?api_key=137392fa767145fe2c94e3d7d6f27c50" + \
            "&query={}".format(urllib.parse.quote(movie_web)) + \
            "&language={}".format(language)
        request = urllib.request.urlopen(request_url)
        r = json.loads(request.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print(error)
        return
    except urllib.error.URLError as error:
        print(error)
        return
    try:
        movies = [movie["title"] +
                  " (" + movie["release_date"][:4] + ")" for movie in r["results"]]
    except KeyError:
        return
    if not movies:
        return
    movies.insert(0, "Skip")
    movies.insert(1, "Manual search")
    return movies


def getOMDB(movie):
    try:
        movie_web = os.path.splitext(movie)[0]
        request_url = "https://www.omdbapi.com/" + \
            "?s={}".format(urllib.parse.quote(movie_web)) + \
            "&apikey=2df782b"
        request = urllib.request.urlopen(request_url)
        r = json.loads(request.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print(error)
        return
    except urllib.error.URLError as error:
        print(error)
        return
    try:
        movies = [movie["Title"] +
                  " (" + movie["Year"] + ")" for movie in r["Search"]]
    except KeyError:
        return
    if not movies:
        return
    movies.insert(0, "Skip")
    movies.insert(1, "Manual search")
    return movies
