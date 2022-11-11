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