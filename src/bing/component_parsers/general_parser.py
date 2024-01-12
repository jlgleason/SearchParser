import bs4


class GeneralParser:
    def __init__(self, cmpt: bs4.element.Tag, cmpt_type: str, cmpt_rank: int):
        """parses general component

        Args:
            cmpt (bs4.element.Tag): BeautifulSoup Tag element
            cmpt_type (str): component type
            cmpt_rank (int): component rank
        """
        self.cmpt = cmpt
        self.results = {
            "type": cmpt_type,
            "cmpt_rank": cmpt_rank,
        }

    def parse(self):
        heading = self.cmpt.find("h2")
        self.results["sub_rank"] = 0
        self.results["url"] = self.get_url(heading)
        self.results["title"] = self.get_title(heading)
        return [self.results]

    def get_url(self, heading):
        if heading and heading.find("a"):
            return heading.find("a").get("href")

    def get_title(self, heading):
        if heading:
            return heading.get_text()
