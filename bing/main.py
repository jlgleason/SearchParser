import pprint
import os

import fire
from bs4 import BeautifulSoup

from searcher import search, save_html, load_html
from parser import parse_serp


def main(qry: str, save_dir: str):
    """runs search, prints parsed results

    Args:
        qry (str): query to send to Bing (e.g. ``car insurance")
        save_dir (str): directory to save SERP html
    """
    
    fp = os.path.join(save_dir, f"{'_'.join(qry.split())}.html")
    if os.path.exists(fp):
        print(f"Loading saved html: {qry}")
        html = load_html(fp)
    else:
        print(f"Running new search: {qry}")
        html = search(qry)
        save_html(html, fp)

    soup = BeautifulSoup(html, "lxml")
    results = parse_serp(soup)
    pp = pprint.PrettyPrinter()
    pp.pprint(results)


if __name__ == "__main__":
    fire.Fire(main)
