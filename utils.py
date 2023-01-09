import json
import os


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


def get_new_queries(fp_qrys: str, fp_parsed: str):
    """removes already parsed queries from list of queries to parse

    Args:
        fp_qrys (str): fp queries to search
        fp_parsed (str): fp already parsed

    Returns:
        List[str]: list of new queries to parse
    """
    with open(fp_qrys, "r") as f:
        qrys = f.read().splitlines()

    if os.path.exists(fp_parsed):
        with open(fp_parsed, "r") as f:
            parsed_qrys = [json.loads(l)["qry"] for l in f.readlines()]
        qrys = list(set(qrys).difference(set(parsed_qrys)))

    return qrys
