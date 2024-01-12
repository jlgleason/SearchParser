from .general_parser import GeneralParser


class AdParser(GeneralParser):
    def __init__(self, *args):
        """ parses ad component
        """
        super().__init__(*args)

    def parse(self):
        ad_block = self.cmpt.find("ul")
        if ad_block:
            return [self.parse_ad(i, ad) for i, ad in enumerate(ad_block)]
        else:
            return []

    def parse_ad(self, i, ad):
        self.results["cmpt_rank"] = i
        return self.results | {
            "sub_rank": 0,
            "url": self.get_url(ad),
            "title": self.get_title(ad),
        }

    def get_url(self, ad):
        attribution = ad.find("div", class_="b_attribution")
        if attribution:
            return attribution.find("cite").text
        else:
            return None
    
    def get_title(self, ad):
        title = ad.find("h2")
        if title:
            return title.get_text()
        else:
            return None
