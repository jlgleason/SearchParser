from urllib.parse import quote_plus

from bs4 import BeautifulSoup, Tag
from pyppeteer import launch

from .component_parsers import CMPT_PARSERS


def parse_serp(serp, serp_id: int = None):
    """parse components from SERP

    Args:
        serp: SERP
        serp_id (int): SERP id. Defaults to None.

    Returns:
        List[dict]: parsed components
    """

    if not isinstance(serp, BeautifulSoup):
        serp = BeautifulSoup(serp, "lxml")

    parsed = []
    for cmpt_rank, cmpt in enumerate(serp.find("div", id="ads")):
        cmpt_parser = CMPT_PARSERS["ad"]
        parsed_cmpts = cmpt_parser(cmpt, "ad", cmpt_rank).parse()
        parsed.extend(parsed_cmpts)
    offset = len(parsed)

    # final 2 elements in links do not correspond to components
    for cmpt_rank, cmpt in enumerate(serp.find("div", id="links").contents[:-2]):
        cmpt_type = classify_type(cmpt)
        cmpt_parser = CMPT_PARSERS[cmpt_type]
        parsed_cmpts = cmpt_parser(cmpt, cmpt_type, cmpt_rank + offset).parse()
        parsed.extend(parsed_cmpts)

    for serp_rank, cmpt in enumerate(parsed):
        cmpt["serp_rank"] = serp_rank
        cmpt["serp_id"] = serp_id

    return parsed


def classify_type(cmpt: Tag):
    """classifies component type

    Args:
        cmpt (Tag): html element

    Returns:
        str: component type
    """
    if "nrn-react-div" in cmpt["class"]:
        return "general"
    else:
        return "unknown"


async def search(qry: str):
    """submits a query to DuckDuckGo using pyppeteer

    Args:
        qry (str): search query

    Returns:
        bytes: response content
    """

    browser = await launch({"headless": False})
    page = await browser.newPage()
    await page.goto(f"https://duckduckgo.com/?q={quote_plus(qry)}")
    html = await page.content()
    await browser.close()
    return html
