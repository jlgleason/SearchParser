import re
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag

from .component_parsers import CMPT_PARSERS


def parse_lang(soup: BeautifulSoup):
    return soup.find("html").attrs["lang"]


def parse_qry(soup: BeautifulSoup):
    # easier to get from URL with parse_qs(urlparse(url).query)["q"]
    return re.sub(r" - Search$", "", soup.find("title").get_text())


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

    # final 2 elements in b_results do not correspond to components
    parsed = []
    for cmpt_rank, cmpt in enumerate(serp.find("ol", id="b_results").contents[:-2]):
        cmpt_type = classify_type(cmpt)
        cmpt_parser = CMPT_PARSERS[cmpt_type]
        parsed_cmpts = cmpt_parser(cmpt, cmpt_type, cmpt_rank).parse()
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
    if "b_algo" in cmpt["class"]:
        return "general"
    elif "b_ad" in cmpt["class"]:
        return "ad"
    else:
        return "unknown"


def search(qry: str):
    """submits a query to Bing using requests

    Args:
        qry (str): search query

    Returns:
        bytes: response content
    """

    return requests.get(
        f"https://www.bing.com/search",
        params={
            "q": qry,
            "form": "QBLH",
        },  # need the form param to get a response with ads
        headers={
            "Host": "www.bing.com",
            "Referer": f"https://www.bing.com/",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "en-US,en;q=0.5",
        },
        timeout=10,
    ).content
