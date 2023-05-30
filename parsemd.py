#!venv/bin/python
## TODO:: add logging support
"""
Python script to convert markdown articles located in the markdown directory to html.
Then move the html to the templates directory and update the articles.json file in the js
directory
"""
import bs4, logging
from markdown import Markdown
from pathlib import Path
from json import loads, dumps
from time import strftime

md_obj = Markdown(extensions = ["fenced_code"], output_format = "html", tab_length = 4)
def save_article_to_json(name : str, date : str):

    articles = Path(__file__).parent / "static" / "js" / "articles.js"
    if not articles.exists():

        raise OSError("object articles.js not found in js directory")

    if not articles.is_file():

        raise OSError("object articles.js in js directory is not a file")

    add_to_json = True
    json_str = ""

    js_lines = articles.read_text().split('\n')
    js_lines[0] = js_lines[0].split('=')[1]
    for line in js_lines:

        json_str += f"{line}\n"

    json_data = loads(json_str)
    for pos in range(len(json_data)):

        if json_data[pos].get("name") == name:

            json_data[pos] = {"name" : name, "date" : date}
            add_to_json = False

    if add_to_json:

        json_data.append({"name" : name, "date" : date})

    articles_file = articles.open("w+")

    js_str = f"const articlesData = {dumps(json_data, indent=4)}"
    articles_file.write(js_str)

    articles_file.close()

def rm_article(name : str):

    articles = Path(__file__).parent / "static" / "js" / "articles.js"
    article = Path(__file__).parent / "static" / "templates" / name
    if not articles.exists():

        raise OSError("object articles.js not found in js directory")

    if not articles.is_file():

        raise OSError("object articles.js in js directory is not a file")

    if not article.exists():

        raise OSError(f"object {name} not found in templates directory")

    if not article.is_file():

        raise OSError(f"object {name} in templates directory is not a file")

    article.unlink() ## delete html file
    ## update article.json
    json_str = ""

    js_lines = articles.read_text().split('\n')
    js_lines[0] = js_lines[0].split('=')[1]
    for line in js_lines:

        json_str += f"{line}\n"

    json_data = loads(json_str)
    for pos in range(len(json_data)):

        if json_data[pos].get("name") == name.split('.')[0]:

            del json_data[pos]

    articles_file = articles.open("w+")

    js_str = f"const articlesData = {dumps(json_data, indent=4)}"
    articles_file.write(js_str)

    articles_file.close()

def save_article_doc(name : str, article_html : str) -> str :

    main_name = name.split('.')[0]
    update_date = strftime("%b %d %Y")
    home_html = Path(__file__).parent / "static" / "templates" / "home.html"
    soup = bs4.BeautifulSoup(home_html.read_text(), "html.parser")

    ## trim home_html
    for tag in soup.html:

        if tag.name == "script":

            if tag.get("src") == "../js/home.js":

                tag["src"] = "../js/article.js"

    soup.html.append(bs4.BeautifulSoup("""
    <script src="../js/highlight.min.js"></script>
    <script>hljs.highlightAll();</script>
    """, "html.parser"))

    for tag in soup.html.head:

        if tag.name == "title":

            tag.string = main_name ## set title as doc name

        elif tag.name == "link":

            if tag.get("href") == "../css/home.css":

                tag["href"] = "../css/article.css"

        elif tag.name == "meta":

            if tag.get("property") == "og:description":

                tag["content"] = f"Article {main_name} on C-NERD's blog" ## update description

    soup.html.head.append(bs4.BeautifulSoup("""
    <link rel="stylesheet" href="../css/default.min.css">
    """, "html.parser"))

    soup.html.body.main.extract() ## remove main tag in body tag
    soup.html.body.append(bs4.BeautifulSoup(f"""<main id = "article_content">
    <span id = "article_meta">
        <h1>{main_name}</h1>
        <em>{update_date}</em>
    </span>
    <span id = "article">
        {article_html}
    </span>
    </main>""", "html.parser")) ## add article data as main tag to body tag

    article_file = Path(__file__).parent / "static" / "templates" / name
    article_file_obj = article_file.open("w+")
    article_file_obj.write(soup.prettify())

    article_file_obj.close()
    save_article_to_json(main_name, update_date)

if "__main__" == __name__:

    import argparse

    parser = argparse.ArgumentParser("parsemd", usage = "parsemd.py <options>", description = "Script to convert markdown articles to html")
    
    parser.add_argument("-a", "--addArticle", action = "store_true", help = "convert markdown to html and add as new article")
    parser.add_argument("-r", "--rmArticle", action = "store_true", help = "rm article's data from article.json and delete article's html file")
    parser.add_argument("--article", type = str, help = "name of article's markdown / html file")

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

        md_file = Path(__file__).parent / "markdown" / args.article
        if not md_file.exists():

            print(f"object {args.article} does not exists in the markdown directory")
            quit(1)

        if not md_file.is_file():

            print(f"object {args.article} is not a file object")
            quit(1)

        html = md_obj.convert(md_file.read_text())
        html_name = args.article.split('.')[0] + ".html"
        save_article_doc(html_name, html)   ## save md as html file

    elif args.rmArticle:

        rm_article(args.article)
