import os
import pprint

import fire
from bs4 import BeautifulSoup

from bing import bing
from searcher import search
from utils import load_html, save_html


PARSER_MAP = {
    "bing": bing.parse_serp,
}


def main(
    sengine: str,
    qry: str,
    save_dir: str = None,
):
    """runs query on search engine, saves html, prints parsed results

    Args:
        sengine (str): search engine
        qry (str): query (e.g. ``car insurance")
        save_dir (str): directory to save SERP html. Defaults to f"{sengine}/serps".
    """

    if not save_dir:
        save_dir = f"{sengine}/serps"
    fp = os.path.join(save_dir, f"{'_'.join(qry.split())}.html")

    if os.path.exists(fp):
        print(f"Loading saved html: {qry}")
        html = load_html(fp)
    else:
        print(f"Running new search: {qry}")
        if sengine.lower() not in PARSER_MAP.keys():
            raise ValueError(f"'senginge' must be one of {list(PARSER_MAP.keys())}")
        html = search(sengine.lower(), qry)
        save_html(html, fp)

    soup = BeautifulSoup(html, "lxml")
    results = PARSER_MAP[sengine.lower()](soup)
    pp = pprint.PrettyPrinter()
    pp.pprint(results)


if __name__ == "__main__":
    fire.Fire(main)
