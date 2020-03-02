import os
import re

from PyInquirer import print_json, prompt

from movie_manager.database import getMovies, manualSearch


def rename(movie, db, language):
    abspath = os.path.abspath(movie)
    dirname = os.path.dirname(abspath)
    filename_w_ext = os.path.basename(abspath)
    filename_wo_ext = os.path.splitext(filename_w_ext)[0]
    filename_ext = os.path.splitext(filename_w_ext)[1]
    filename_wo_year = re.sub(r"\((.*?)\)", "", filename_wo_ext)

    movies = getMovies(filename_wo_year, db, language)

    while True:
        if not movies:
            questions = [
                {
                    'type': 'list',
                    'name': 'whattodo',
                    "qmark": "[!]",
                    'message': filename_w_ext,
                    "choices": ["Skip", "Manual search"]
                }
            ]
            answer = prompt(questions)["whattodo"]
            if answer == "Skip":
                return
            elif answer == "Manual search":
                questions = {
                    'type': 'input',
                    "qmark": "[?]",
                    'name': 'usermovie',
                    'message': 'Manual search:',
                }
                answer = prompt(questions)["usermovie"]
                movies = manualSearch(answer, language)
                continue
        questions = [
            {
                'type': 'list',
                'name': 'movie',
                "qmark": "[?]",
                'message': filename_w_ext,
                "choices": movies
            }
        ]
        answer = prompt(questions)["movie"]
        if answer == "Skip":
            return
        elif answer == "Manual search":
            questions = {
                'type': 'input',
                "qmark": "[?]",
                'name': 'usermovie',
                'message': 'Manual search:',
            }
            answer = prompt(questions)["usermovie"]
            movies = manualSearch(answer, language)
            continue
        break

    selected_movie = answer.replace(":", "-")
    os.rename(abspath, os.path.join(dirname, selected_movie + filename_ext))
