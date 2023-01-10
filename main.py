import argparse
import asyncio
import pprint
import json
from requests.models import PreparedRequest

from pyppeteer import launch, browser

from bing import bing
from ddg import ddg
from utils import get_new_queries


PARSE_FUNCS = {"ddg": ddg.parse_serp, "bing": bing.parse_serp}
BASE_URLS = {
    "bing": "https://www.bing.com/search",
    "ddg": "https://duckduckgo.com",
}
PARAMS = {
    "bing": {"form": "QBLH"},  # need the form param to get a response with ads
    "ddg": {},
}


def build_url(sengine: str, qry: str):
    """build search url from base, qry, params"""
    req = PreparedRequest()
    req.prepare_url(BASE_URLS[sengine], {"q": qry} | PARAMS[sengine])
    return req.url


async def crawl(sengine: str, browser: browser.Browser, qry: str, fp_save: str):
    """runs a search and parses the results"""

    page = await browser.newPage()
    user_agent = await page.evaluate("() => navigator.userAgent")
    await page.setUserAgent(user_agent.replace("HeadlessChrome", "Chrome"))
    await page.goto(build_url(sengine, qry))
    html = await page.content()
    await page.close()

    results = PARSE_FUNCS[sengine](html, qry=qry)
    if fp_save:
        for result in results:
            fp_save.write(json.dumps(result))
            fp_save.write("\n")
    else:
        pp = pprint.PrettyPrinter()
        pp.pprint(results)


async def main(
    sengine: str,
    fp_qrys: str,
    fp_parsed: str = None,
    n_threads: int = 10,
    test: bool = False,
):
    """runs queries in 'fp_qrys' on 'sengine', saves parsed results to 'fp_parsed'"""

    if test:
        qrys = [fp_qrys]
        fp = None
    else:
        qrys = get_new_queries(fp_qrys, fp_parsed)
        fp = open(fp_parsed, "a")

    try:
        i = 0
        while i <= len(qrys):
            browser = await launch()
            tasks = [
                asyncio.ensure_future(crawl(sengine, browser, qry, fp))
                for qry in qrys[i : i + n_threads]
            ]
            await asyncio.gather(*tasks)
            await browser.close()
            i += n_threads
            num = min(i, len(qrys))
            print(f"Crawled {num} of {len(qrys)} queries ({round(num, 3)})")
    except:
        await browser.close()

    if not test:
        fp.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crawl and parse Bing or DuckDuckGo SERPs"
    )
    parser.add_argument(
        "-s", "--sengine", default="bing", type=str, help="'bing' or 'ddg'"
    )
    parser.add_argument(
        "-t",
        "--test",
        action=argparse.BooleanOptionalAction,
        help="whether in testing mode",
        default=False,
    )
    parser.add_argument(
        "-q",
        "--fp_qrys",
        type=str,
        help="If not in testing mode, this argument will be treated as a filename for newline-delimited queries. If in testing mode, this argument will be treated as the query string.",
    )
    parser.add_argument(
        "--fp_parsed", type=str, help="Save parsing results to this file", default=None
    )
    parser.add_argument(
        "--n_threads",
        type=int,
        help="Number of queries to run in parallel tabs before restarting browser",
        default=10,
    )
    args = parser.parse_args()

    asyncio.run(
        main(args.sengine, args.fp_qrys, args.fp_parsed, args.n_threads, args.test)
    )
