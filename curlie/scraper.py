import requests
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
        headers={
            "Host": "www.curlie.org",
            "Referer": "https://www.curlie.org/",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Accept-Encoding": "gzip,deflate",
            "Accept-Language": "en-US,en;q=0.5",
        },
        timeout=10,
    ).text
    return BeautifulSoup(r, "html.parser")


def get_sites(html: BeautifulSoup, category: str) -> dict:
    """
    Scrapes sites from Curlie page
    :param html: BeautifulSoup-parsed html
    :param category: current category
    :return: dictionary mapping business name to url and category
    """
    sites = {}
    start = html.find_all("div", class_="site-title")
    if start:
        for each in start:
            site = each.find("a", target="_blank")
            if site not in sites:
                sites[site.text] = (site.get("href"), category)
    return sites


def get_subcategories(html: BeautifulSoup, sesh: requests.Session) -> None:
    """
    Gets subcategories for each site and calls recursively
    :param html: BeautifulSoup parsed html
    :param sesh: requests session
    :return: all scraped sites
    """
    start = html.find_all("div", class_="cat-list results leaf-nodes")
    if start is not None:
        for each in start:
            cat_cmpts = each.find_all("div", class_="cat-item")
            for cmpt in cat_cmpts:
                category = cmpt.find("a").get("href")
                print("Searching subcategories...\n")
                page_text = search(sesh, category).find("div")
                print("Finding sites...\n")
                sites = (get_sites(page_text, category))
                print("Writing to file...\n")
                write_to_file(sites)
                get_subcategories(page_text, sesh)
    else:
        print("Reached end of subcategories... Done!\n")
        return


def write_to_file(sites: dict) -> None:
    """
    Writes sites to file by name, url, and category
    :param sites: list of scraped sites
    :return: nothing
    """
    with open("results.txt", mode="a") as outfile:
        for each in sites:
            outfile.write("{\"Name\": \"" + each + "\", \"URL\": \"" + sites.get(each)[0]
                          + "\", \"Category\": \"" + sites.get(each)[1] + "\"}\n\n")
    outfile.close()


def main():
    r = requests.session()

    category = "Business"
    page_text = search(r, category).find("div")
    get_subcategories(page_text, r)

    category = "Shopping"
    page_text = search(r, category).find("div")
    get_subcategories(page_text, r)


if __name__ == "__main__":
    main()
