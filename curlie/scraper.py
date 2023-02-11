import json
import queue
import requests
from bs4 import BeautifulSoup

"""
Curlie Scraper 
Records sites under each category and scrapes subcategories, 
Then performs the same process on all subcategories
"""

VISITED = set()
QUEUE = queue.Queue()


def search(sesh: requests.Session, category: str):
    """submits a query to Curlie using requests
    Args:
        sesh (requests.Session): requests session
        category (str): category
    Returns:
        BeautifulSoup: html-parsed response content
    """
    r = sesh.get(
        "https://www.curlie.org/" + category,
        timeout=30,
    ).text
    return BeautifulSoup(r, "lxml")


def get_sites(html: BeautifulSoup, category: str) -> list:
    """
    Scrapes sites from Curlie page
    :param html: BeautifulSoup-parsed html
    :param category: current category
    :return: dictionary mapping business name to url and category
    """
    sites = []
    start = html.find_all("div", class_="site-title")
    if start:
        for each in start:
            site = each.find("a", target="_blank")
            if site not in sites:
                current = {
                    "Name": site.text,
                    "URL": site.get("href"),
                    "Category": category,
                }
                sites.append(current)
    return sites


def get_subcategories(html: BeautifulSoup) -> list:
    """
    Gets subcategories for each site and calls recursively
    :param html: BeautifulSoup parsed html
    :param sesh: requests session
    :return: all scraped sites
    """
    start = html.find_all("div", class_="cat-list results leaf-nodes")
    all_cats = []
    if start is not None:
        for each in start:
            cat_cmpts = each.find_all("div", class_="cat-item")
            cats = [cmpt.find("a").get("href") for cmpt in cat_cmpts]
            all_cats.extend(cats)
    return all_cats


def write_to_file(sites: list) -> None:
    """
    Writes sites to file by name, url, and category
    :param sites: list of scraped sites
    :return: nothing
    """
    with open("results2.txt", mode="a") as outfile:
        for site in sites:
            outfile.write(json.dumps(site))
            outfile.write("\n")
    outfile.close()


def scrape_category(sesh, count):
    """
    1) requests category, 2) gets subcategories, 3) gets sites, 4) writes sites to file
    :param sesh: requests session
    :param category: current category
    :param top_level_cats: only scrape categories under these top levels
    :return: nothing
    """
    category = QUEUE.get()

    # check if category already visited
    if category in VISITED:
        return

    print(f"Scraping {category}")
    if count == 50:
        sesh.close()
        sesh = requests.session
        count = 0

    count += 1
    page_text = search(sesh, category).find("div")

    sites = get_sites(page_text, category)
    write_to_file(sites)
    VISITED.add(category)


    # get subcategories, recursively scrape
    sub_cats = get_subcategories(page_text)
    for sub_cat in sub_cats:
        print(f"Just added {category}")
        QUEUE.put(sub_cat)
    # scrape_category(sesh, count)


def main():
    sesh = requests.session()
    count = 0

    category = "/en/Business/Accounting/"
    QUEUE.put(category)
    print(f"Just added {category}")

    while QUEUE.qsize() > 0:
        scrape_category(sesh, count)

    """
    category = "Shopping"
    page_text = search(r, category).find("div")
    get_subcategories(page_text, r)
    """


if __name__ == "__main__":
    main()

