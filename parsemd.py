#!/bin/python3

"""
Python script to convert markdown articles located in the markdown folder to html.
Then move the html to the templates folder and update the articles.json file in the js
folder
"""

if "__main__" == __name__:

    import argparse

    parser = argparse.ArgumentParser("parsemd", usage = "parsemd.py <options>", description = "Script to convert markdown articles to html")
    
    parser.add_argument("-a", "--addArticle", action = "store_true", help = "convert markdown to html and add as new article")
    parser.add_argument("-r", "--rmArticle", action = "store_true", help = "rm article's data from article.json and delete article's html file")
    parser.add_argument("--article", type = str, help = "file name of article's markdown")

    args = None
    try:

        args = parser.parse_args()

    except Exception:

        parser.print_help()
        quit(1) ## Failure

    if not args.article:

        print("option --article was not given")
        quit(1) ## Failure

    if args.addArticle:

        pass

    elif args.rmArticle:

        pass