import os
import pprint
import argparse
import asyncio

from bs4 import BeautifulSoup

from bing import bing
from ddg import ddg
from utils import load_html, save_html


def test_bing(qry: str, save_dir: str = None):
    """runs qry on Bing, saves html, prints parsed results

    Args:
        qry (str): query (e.g. ``car insurance")
        save_dir (str): directory to save SERP html. Defaults to f"bing/serps".
    """

    if not save_dir:
        save_dir = "bing/serps"
    fp = os.path.join(save_dir, f"{'_'.join(qry.split())}.html")

    if os.path.exists(fp):
        print(f"Loading saved html: {qry}")
        html = load_html(fp)
    else:
        html = bing.search(qry)
        save_html(html, fp)

    soup = BeautifulSoup(html, "lxml")
    results = bing.parse_serp(soup)
    pp = pprint.PrettyPrinter()
    pp.pprint(results)


async def test_ddg(qry: str, save_dir: str = None):
    """runs qry on DuckDuckGo, saves html, prints parsed results

    Args:
        qry (str): query (e.g. ``car insurance")
        save_dir (str): directory to save SERP html. Defaults to f"ddg/serps".
    """
    
    if not save_dir:
        save_dir = "ddg/serps"
    fp = os.path.join(save_dir, f"{'_'.join(qry.split())}.html")

    if os.path.exists(fp):
        print(f"Loading saved html: {qry}")
        html = load_html(fp)
    else:
        html = await ddg.search(qry)
        save_html(str.encode(html), fp)
    
    soup = BeautifulSoup(html, "lxml")
    results = ddg.parse_serp(soup)
    pp = pprint.PrettyPrinter()
    pp.pprint(results)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawl and parse Bing or DuckDuckGo SERPs"
    )
    parser.add_argument(
        "-s",
        "--sengine",
        default="bing",
        type=str,
    )
    parser.add_argument(
        "-q",
        "--qry",
        type=str,
    )
    parser.add_argument(
        "-d",
        "--save_dir",
        type=str,
        help="Save SERP html to this directory"
    )
    # TODO test argument
    args = parser.parse_args()
    
    if args.sengine == "bing":
        test_bing(args.qry, args.save_dir)
    elif args.sengine == "ddg":
        asyncio.run(test_ddg(args.qry, args.save_dir))
