import re
import requests

from bs4 import BeautifulSoup
from bs4.element import Tag

from .component_parsers import CMPT_PARSERS

# Treats every component as the same, extracts two types of info:
# what kind of component (ad or not)
# and what the url was (to classify the domain)
# find id=b_results and iterate through descendants
# API ad client: Fix US region, English sample, match type, ad position


def open_file(filename: str):
    try:
        with open(filename, mode="r") as infile:
            soup = BeautifulSoup(infile, "lxml")
            return soup
    except OSError:
        print("A file error occured")


# Appends new parsed components to components file
def save_data(newfile: str, parsed_data):
    with open(newfile, mode="a") as outfile:
        for each in parsed_data:
            outfile.write(str(each) + "\n")
    outfile.close()


# Saves prettified data
def save_pretty(newfile: str, soup):
    with open(newfile, mode="a") as outfile:
        for line in soup:
            outfile.write(str(line))
    outfile.close()


# Parses components in b_results tree and also searches for id tags
def parse_components(soup):
    parsed_data = []
    for cmpt in soup.find("ol", id="b_results"):
        parsed_data.append(cmpt["class"])
        if cmpt.has_attr("id"):
            parsed_data.append(cmpt["id"])
    return parsed_data


def main():
    # pretty_soup = open_file("bing_data.txt")
    # save_pretty("bing_output.txt", pretty_soup)
    soup = open_file("bing_data.txt")
    parsed_data = parse_components(soup)
    save_data("b_components.txt", parsed_data)


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


# Classifies component type
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


if __name__ == "__main__":
    main()
