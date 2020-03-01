from __future__ import print_function, unicode_literals

import argparse
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request

from PyInquirer import print_json, prompt


def getTMDB(movie, lang):
    # lets try to get some infos from the movie database
    try:
        if not lang:
            lang = "en-US"
        movie_web = os.path.splitext(movie)[0]
        request_url = "https://api.themoviedb.org/3/search/movie" + \
            "?api_key=137392fa767145fe2c94e3d7d6f27c50" + \
            "&query={}".format(urllib.parse.quote(movie_web)) + \
            "&language={}".format(lang)
        request = urllib.request.urlopen(request_url)
        r = json.loads(request.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        print(error)
        return
    except urllib.error.URLError as error:
        print(error)
        return
    try:
        # get all movies with year from response
        movies = [movie["title"] +
                  " (" + movie["release_date"][:4] + ")" for movie in r["results"]]
    except KeyError:
        return

    if not movies:
        # shit, we couldn't find movies
        return

    # good! we got some movies. lets add skip and manual search options
    movies.insert(0, "Skip")
    movies.insert(1, "Manual search")
    return movies


def getOMDB(movie):
    # lets try to get some infos from open movie database
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
        # get all movies with year from response
        movies = [movie["Title"] +
                  " (" + movie["Year"] + ")" for movie in r["Search"]]
    except KeyError:
        return

    if not movies:
        # shit, we couldn't find movies
        return

    # good! we got some movies. lets add skip and manual search options
    movies.insert(0, "Skip")
    movies.insert(1, "Manual search")
    return movies


def manualSearch(lang):
    # db results were shit, so let the user search for a custom string
    questions = {
        'type': 'input',
        "qmark": "[?]",
        'name': 'usermovie',
        'message': 'Manual search:',
    }
    answer = prompt(questions)["usermovie"]
    # search for string in db's
    movies = getTMDB(answer, lang)
    if not movies:
        movies = getOMDB(answer)
    if not movies:
        return
    return movies


def rename(db, lang, movie):
    # split the extension and name from file and remove (year) for search improvements
    movie_ext = os.path.splitext(movie)[1]
    movie_name = re.sub(
        r"\((.*?)\)", "", os.path.splitext(os.path.basename(movie))[0])

    # set db if user didn't set it and check db's for movies
    if not db:
        db = "all"

    # only check tmdb
    if db.lower() == "tmdb":
        print("[!] Searching on tmdb")
        movies = getTMDB(movie_name, lang)
    # only check omdb
    if db.lower() == "omdb":
        print("[!] Searching on omdb")
        movies = getOMDB(movie_name)

    # check all
    if db.lower() == "all":
        print("[!] Searching on tmdb")
        movies = getTMDB(movie_name, lang)
        if not movies:
            print("[!] Searching on omdb")
            movies = getOMDB(movie_name)

    while True:
        if not movies:
            # shit, we couldn't find movies
            questions = [
                {
                    'type': 'list',
                    'name': 'whattodo',
                    "qmark": "[!]",
                    'message': os.path.basename(movie),
                    "choices": ["Skip", "Manual search"]
                }
            ]
            answer = prompt(questions)["whattodo"]
            # ask to skip movie our do a manual search
            if answer == "Skip":
                return
            elif answer == "Manual search":
                movies = manualSearch(lang)
                continue

        # good! we got some movies
        questions = [
            {
                'type': 'list',
                'name': 'movie',
                "qmark": "[?]",
                'message': os.path.basename(movie),
                "choices": movies
            }
        ]
        answer = prompt(questions)["movie"]

        # ask to skip movie our do a manual search
        if answer == "Skip":
            return
        elif answer == "Manual search":
            movies = manualSearch(lang)
            continue
        break

    # lets replace : with - from file names
    sel_movie = answer.replace(":", "-")
    # and actually rename the file
    os.rename(movie, os.path.join(
        os.path.dirname(movie), sel_movie + movie_ext))


def main(args):
    for i in args.input:
        # check if input is dir
        if os.path.isdir(i):
            files_in_path = [f for f in os.listdir(
                i) if os.path.isfile(os.path.join(i, f))]
            # loop though files in dir
            for item in files_in_path:
                print("\n")
                print("[!]", files_in_path.index(item)+1,
                      "of", str(len(files_in_path)) + ":", item)
                # rename them
                rename(args.database, args.language, os.path.abspath(
                    os.path.join(i, item)))
        # check if input is file
        elif os.path.isfile(i):
            print("\n")
            rename(args.database, args.language, i)
        else:
            print("[!] Path or file not found.")


if __name__ == "__main__":
    # Handles argmuments passed to mm
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Input file or directory", nargs="*", required=True)
    parser.add_argument(
        "-db", "--database", help="\"tmdb\" and \"omdb\" so far. Leave blank for all.")
    parser.add_argument(
        "-l", "--language", help="Searche databases in this language. Default is en-US. OMDB doesn't support language support."
    )
    args = parser.parse_args()
    # all right, lets get to it
    if not args.input:
        print(args)
    else:
        main(args)
