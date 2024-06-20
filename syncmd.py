#!/bin/python
from pathlib import Path
from os import listdir
from os.path import getmtime
from json import dump, dumps

class SyncMd:

    def __init__(self) -> None:
        
        articles_dir = Path(__name__).parent / "static/articles"
        self.meta_data = []
        for article in listdir(str(articles_dir)):
            
            article = articles_dir / article
            if not article.is_file():

                continue

            elif article.name.split('.')[-1] != "md":

                continue

            self.meta_data.append(
                {
                    "title" : article.name.split('.')[0],
                    "content" : article.read_text(),
                    "date" : int(getmtime(str(article)))
                }
            )

    def save_meta(self, path):

        with open(Path(__name__).parent / path, "w") as file:

            file.write(dumps(self.meta_data, indent = 2))
            file.flush()

    def __del__(self):

        pass

if __name__ == "__main__":
    
    print("reading meta ...")
    s = SyncMd()
    print("saving meta ...")
    s.save_meta("metadata.json")

