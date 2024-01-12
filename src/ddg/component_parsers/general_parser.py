import bs4


class GeneralParser:

    def __init__(self, cmpt: bs4.element.Tag, cmpt_type: str, cmpt_rank: int):
        """ parses general component from DDG SERP
        
        Args:
            cmpt (bs4.element.Tag): BeautifulSoup Tag element
            cmpt_type: (str) component type 
        """
        self.cmpt = cmpt
        self.results = {"type": cmpt_type, "cmpt_rank": cmpt_rank}

    def parse(self):
        self.results["sub_rank"] = 0
        self.attr = self.cmpt.find("a", attrs={"data-testid": "result-title-a"})
        self.results["url"] = self.get_url()
        self.results["title"] = self.get_title()
        return [self.results]

    def get_url(self):
        if self.attr:
            return self.attr.get("href")
        else:
            return None

    def get_title(self):
        if self.attr:
            return self.attr.get_text()
        else:
            return None