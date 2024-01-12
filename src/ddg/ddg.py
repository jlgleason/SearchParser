from urllib.parse import quote_plus
import json

from bs4 import BeautifulSoup, Tag
from pyppeteer import browser

from .component_parsers import CMPT_PARSERS


def parse_serp(serp, serp_id: int = None, qry: str = None):
    """parse components from SERP

    Args:
        serp: SERP
        serp_id (int): SERP id. Defaults to None.
        qry (str): query. Defaults to None.

    Returns:
        List[dict]: parsed components
    """

    if not isinstance(serp, BeautifulSoup):
        serp = BeautifulSoup(serp, "lxml")

    parsed = []
    for cmpt_rank, cmpt in enumerate(serp.find("ol", class_="react-results--main")):
        cmpt_type = classify_type(cmpt)
        cmpt_parser = CMPT_PARSERS[cmpt_type]
        parsed_cmpts = cmpt_parser(cmpt, cmpt_type, cmpt_rank).parse()
        parsed.extend(parsed_cmpts)

    for serp_rank, cmpt in enumerate(parsed):
        cmpt["serp_rank"] = serp_rank
        cmpt["serp_id"] = serp_id
        cmpt["qry"] = qry

    return parsed


def classify_type(cmpt: Tag):
    """classifies component type

    Args:
        cmpt (Tag): html element

    Returns:
        str: component type
    """
    data_type = cmpt.get("data-layout")
    if data_type == "organic":
        return "general"
    elif data_type == "ad":
        return "ad"
    else:
        return "unknown"


async def search(browser: browser.Browser, qry: str):
    """submits a query to DuckDuckGo using pyppeteer

    Args:
        browser (browser.Browser): chrome browser
        qry (str): search query

    Returns:
        bytes: response content
    """

    page = await browser.newPage()
    user_agent = await page.evaluate("() => navigator.userAgent")
    await page.setUserAgent(user_agent.replace("HeadlessChrome", "Chrome"))
    await page.goto(f"https://duckduckgo.com/?q={quote_plus(qry)}")
    html = await page.content()
    await page.close()
    return html


async def crawl(browser: browser.Browser, qry: str, fp_save: str):
    """runs search, parses html, saves to file

    Args:
        browser (browser.Browser): chrome browser
        qry (str): search query
        fp_save (str): save file
    """

    html = await search(browser, qry)
    results = parse_serp(html, qry=qry)
    for result in results:
        fp_save.write(json.dumps(result))
        fp_save.write("\n")
