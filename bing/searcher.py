import requests


HEADERS = {
    "Host": "www.bing.com",
    "Referer": "https://www.bing.com/",
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:58.0) Gecko/20100101 Firefox/58.0",
    "Accept-Encoding": "gzip,deflate,br",
    "Accept-Language": "en-US,en;q=0.5",
}


def search(qry: str):
    """runs a search on Bing

    Args:
        qry (str): search query

    Returns:
        bytes: response content
    """

    sesh = requests.Session()
    sesh.headers.update(HEADERS)
    try:
        res = sesh.get(
            "https://www.bing.com/search",
            params={
                "q": qry,
                "form": "QBLH",
            },  # need the form param to get a response with ads
            timeout=10,
        )
    except Exception as e:
        print(e)
    sesh.close()
    return res.content


def save_html(html: bytes, fp: str):
    """saves response content to file

    Args:
        html (bytes): html response
        fp (str): filepath
    """
    with open(fp, "wb") as f:
        f.write(html)


def load_html(fp: str):
    """loads response content from file

    Args:
        fp (str): filepath

    Returns:
        bytes: html response
    """
    with open(fp, "rb") as f:
        html = f.read()
    return html
