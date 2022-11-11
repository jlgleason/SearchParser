import requests

DOMAINS = {
    "bing": "www.bing.com"
}

PAGES = {
    "bing": "search"
}

PARAMS = {
    "bing": {"form": "QBLH"} # need the form param to get a response with ads
}

# TODO turn this into a class that uses requests.Session
def search(sengine: str, qry: str):
    """runs a query on a specific search engine

    Args:
        sengine (str): search engine
        qry (str): search query

    Returns:
        bytes: response content
    """

    return requests.get(
        f"https://{DOMAINS[sengine]}/{PAGES[sengine]}",
        params={"q": qry} | PARAMS[sengine],
        headers={
            "Host": DOMAINS[sengine],
            "Referer": f"https://{DOMAINS[sengine]}/",
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
            "Accept-Encoding": "gzip,deflate,br",
            "Accept-Language": "en-US,en;q=0.5", 
        },
        timeout=10,
    ).content