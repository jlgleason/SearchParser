import argparse
import asyncio
import requests

from pyppeteer import launch
import tqdm 

from src.bing import bing
from src.ddg import ddg
from src.utils import get_new_queries


def run_bing(fp_qrys: str, fp_parsed: str):
    """runs queries on Bing, saves parsed results

    Args:
        fp_qrys (str): filepath with line-delimited queries.
        fp_parsed (str): filepath to save parsed results.
    """

    qrys = get_new_queries(fp_qrys, fp_parsed)
    
    try:
        fp = open(fp_parsed, "a")
        sesh = requests.Session()
        for qry in tqdm.tqdm(qrys):
            bing.crawl(sesh, qry, fp)
    finally:
        sesh.close()
        fp.close()


async def run_ddg(fp_qrys: str, fp_parsed: str, n_threads: int = 10):
    """runs queries on DuckDuckGo, saves parsed results

    Args:
        fp_qrys (str): filepath with line-delimited queries.
        fp_parsed (str): filepath to save parsed results.
        n_threads (int): number of queries to parse in parallel tabs. Defaults to 10.
    """

    qrys = get_new_queries(fp_qrys, fp_parsed)

    try:
        fp = open(fp_parsed, "a")
        i = 0
        while i <= len(qrys):
            print(qrys[i:i+n_threads])
            browser = await launch()
            tasks = [
                asyncio.ensure_future(ddg.crawl(browser, qry, fp))
                for qry in qrys[i:i+n_threads]
            ]
            await asyncio.gather(*tasks)
            await browser.close()
            i += n_threads
            num = min(i, len(qrys))
            print(f'Crawled {num} of {len(qrys)} queries ({round(num/len(qrys), 2)})')
    except:
        await browser.close()
    finally:
        fp.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawl and parse Bing or DuckDuckGo SERPs"
    )
    parser.add_argument(
        "-s", "--sengine", default="bing", type=str, help="'bing' or 'ddg'"
    )
    parser.add_argument("--fp_qrys", type=str, help="newline-delimited file of queries")
    parser.add_argument(
        "--fp_parsed", type=str, help="Save parsing results to this file"
    )
    parser.add_argument(
        "--n_threads", type=int, help="Number of queries to run in parallel for DDG crawling", default=10
    )
    args = parser.parse_args()

    if args.sengine == "bing":
        run_bing(args.fp_qrys, args.fp_parsed)
    elif args.sengine == "ddg":
        asyncio.run(run_ddg(args.fp_qrys, args.fp_parsed, args.n_threads))
