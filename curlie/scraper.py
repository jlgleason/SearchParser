import json
import requests
from requests.adapters import HTTPAdapter
from bs4 import BeautifulSoup

"""
Curlie Scraper 
Records sites under each category and scrapes subcategories, 
Then performs the same process on all subcategories
"""


def search(sesh: requests.Session, qry: str):
    """submits a query to Curlie using requests
    Args:
        sesh (requests.Session): requests session
        qry (str): category
    Returns:
        BeautifulSoup: html-parsed response content
    """
    r = sesh.get(
        "https://www.curlie.org/" + qry,
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
                current = {"Name": site.text, "URL": site.get("href"), "Category": category}
                sites.append(current)
    return sites


def get_subcategories(html: BeautifulSoup, sesh: requests.Session) -> None:
    """
    Gets subcategories for each site and calls recursively
    :param html: BeautifulSoup parsed html
    :param sesh: requests session
    :return: all scraped sites
    """
    start = html.find_all("div", class_="cat-list results leaf-nodes")
    visited = set()
    if start is not None:
        for each in start:
            cat_cmpts = each.find_all("div", class_="cat-item")
            for cmpt in cat_cmpts:
                category = cmpt.find("a").get("href")
                visited.add(category)
        scrape_categories(visited, sesh)
    else:
        print("Reached end of subcategories... Done!\n")
        return


def scrape_categories(categories: set, sesh: requests.Session) -> None:
    """
    Helper function for get_subcategories
    """
    for cat in categories:
        page_text = search(sesh, cat).find("div")
        print("Finding sites in category" + cat + "...\n")
        sites = (get_sites(page_text, cat))
        write_to_file(sites)
        get_subcategories(page_text, sesh)


def write_to_file(sites: list) -> None:
    """
    Writes sites to file by name, url, and category
    :param sites: list of scraped sites
    :return: nothing
    """
    with open("results1.txt", mode="a") as outfile:
        for site in sites:
            outfile.write(json.dumps(site))
            outfile.write("\n")
    outfile.close()


def main():
    r = requests.session()
    r.mount("https://www.curlie.org/", HTTPAdapter(max_retries=5))

    category = "Business/Accounting/"
    page_text = search(r, category).find("div")
    get_subcategories(page_text, r)

    """
    category = "Shopping"
    page_text = search(r, category).find("div")
    get_subcategories(page_text, r)
    """


if __name__ == "__main__":
    main()
