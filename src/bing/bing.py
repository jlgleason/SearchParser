import requests
import json

from bs4 import BeautifulSoup
from bs4.element import Tag

from .component_parsers import CMPT_PARSERS


def parse_lang(soup: BeautifulSoup):
    return soup.find("html").attrs["lang"]


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
    cmpt = serp.find("div", class_="pa_carousel adsMvCarousel")
    if cmpt:
        cmpt_type = "shopping_ads"
        cmpt_parser = CMPT_PARSERS[cmpt_type]
        parsed_cmpts = cmpt_parser(cmpt, cmpt_type, 0).parse()
        parsed.extend(parsed_cmpts)

    if len(parsed):
        offset = parsed[-1]["cmpt_rank"] + 1
    else:
        offset = 0

    for cmpt_rank, cmpt in enumerate(serp.find("ol", id="b_results")):
        cmpt_type = classify_type(cmpt)
        if cmpt_type == "ignore":
            continue
        else:
            cmpt_parser = CMPT_PARSERS[cmpt_type]
            parsed_cmpts = cmpt_parser(cmpt, cmpt_type, cmpt_rank + offset).parse()
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

    if "class" not in cmpt.attrs:
        return "unknown"

    ignore = ["b_msg", "b_pag", "fabcolapse"]
    if any([t in cmpt["class"] for t in ignore]):
        return "ignore"

    if "b_algo" in cmpt["class"]:
        return "general"
    elif "b_ad" in cmpt["class"]:
        if cmpt.find("div", class_="autos_ml_ads_container"):
            return "car_ads"
        else:
            return "ad"
    else:
        return "unknown"


def search(sesh: requests.Session, qry: str):
    """submits a query to Bing using requests

    Args:
        sesh (requests.Session): requests session
        qry (str): search query


    Returns:
        bytes: response content
    """

    return sesh.get(
        "https://www.bing.com/search",
        params={
            "q": qry,
            "form": "QBLH",
        },  # need the form param to get a response with ads
        headers={
            "Host": "www.bing.com",
            "Referer": "https://www.bing.com/",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.5",
        },
        timeout=10,
    ).content


def crawl(sesh: requests.Session, qry: str, fp_save: str):
    """runs search, parses html, saves to file

    Args:
        sesh (requests.Session): requests session
        qry (str): search query
        fp_save (str): save file
    """

    html = search(sesh, qry)
    try:
        results = parse_serp(html, qry=qry)
        for result in results:
            fp_save.write(json.dumps(result))
            fp_save.write("\n")
    except:
        print(f"parsing error for qry: {qry}")
