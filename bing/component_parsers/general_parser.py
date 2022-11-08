import bs4

class GeneralParser:

    def __init__(self, cmpt: bs4.element.Tag, cmpt_type: str, cmpt_rank: int):
        """ parses general component

        Args:
            cmpt (bs4.element.Tag): BeautifulSoup Tag element
            cmpt_type (str): component type
            cmpt_rank (int): component rank
        """
        self.cmpt = cmpt
        self.results = {
            "cmpt_type": cmpt_type,
            "cmpt_rank": cmpt_rank,
        }
    
    def parse(self):    
        self.results["sub_rank"] = 0
        self.results["url"] = self.get_url(self.cmpt)
        self.results["title"] = self.get_title()
        return [self.results]
    
    def get_url(self, cmpt):
        attribution = cmpt.find("div", class_="b_attribution")
        if attribution:
            return attribution.find("cite").text
        else:
            return None
    
    def get_title(self):
        title = self.cmpt.find("div", class_="b_title")
        if title:
            return title.get_text()
        else:
            return None
