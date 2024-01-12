import os
import pprint
import argparse
import asyncio
import requests

from bs4 import BeautifulSoup
from pyppeteer import launch

from src.bing import bing
from src.ddg import ddg
from src.utils import load_html, save_html


def test_bing(qry: str, save_dir: str = None):
    """runs qry on Bing, saves html, prints parsed results

    Args:
        qry (str): query (e.g. ``car insurance")
        save_dir (str): directory to save SERP html. Defaults to f"serps/bing".
    """

    if not save_dir:
        save_dir = "serps/bing"
    os.makedirs(save_dir, exist_ok=True)
    fp = os.path.join(save_dir, f"{'_'.join(qry.split())}.html")

    if os.path.exists(fp):
        print(f"Loading saved html: {qry}")
        html = load_html(fp)
    else:
        with requests.Session() as sesh:
            html = bing.search(sesh, qry)
        save_html(html, fp)

    soup = BeautifulSoup(html, "lxml")
    results = bing.parse_serp(soup)
    pp = pprint.PrettyPrinter()
    pp.pprint(results)


async def test_ddg(qry: str, save_dir: str = None):
    """runs qry on DuckDuckGo, saves html, prints parsed results

    Args:
        qry (str): query (e.g. ``car insurance")
        save_dir (str): directory to save SERP html. Defaults to f"serps/ddg".
    """

    if not save_dir:
        save_dir = "serps/ddg"
    os.makedirs(save_dir, exist_ok=True)
    fp = os.path.join(save_dir, f"{'_'.join(qry.split())}.html")

    if os.path.exists(fp):
        print(f"Loading saved html: {qry}")
        html = load_html(fp)
    else:
        browser = await launch()
        html = await ddg.search(browser, qry)
        await browser.close()
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
        "-d", "--save_dir", type=str, help="Save SERP html to this directory"
    )
    args = parser.parse_args()

    if args.sengine == "bing":
        test_bing(args.qry, args.save_dir)
    elif args.sengine == "ddg":
        asyncio.run(test_ddg(args.qry, args.save_dir))
