from __future__ import print_function, unicode_literals

import argparse
import os

from movie_manager.filehandler import rename


def main(args):
    for input_ in args.input:
        if os.path.isdir(input_):
            files_in_dir = [f for f in os.listdir(
                input_) if os.path.isfile(os.path.join(input_, f))]
            for file_ in files_in_dir:
                abspath = os.path.abspath(os.path.join(input_, file_))
                print("\n")
                print("[!]", files_in_dir.index(file_) + 1,
                      "of", len(files_in_dir))
                rename(abspath, args.database, args.language)
        elif os.path.isfile(input_):
            print("\n")
            rename(input_, args.database, args.language)
        else:
            print("[!] Path or file not found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", help="Input file or directory", nargs="*", required=True)
    parser.add_argument(
        "-db", "--database", help="\"tmdb\" and \"omdb\" so far. Leave blank for all.")
    parser.add_argument(
        "-l", "--language", help="Searche databases in this language. Default is en-US. OMDB doesn't support language support.")
    args = parser.parse_args()

    if not args.input:
        print(args)
    else:
        main(args)
