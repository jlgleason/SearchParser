import bs4
from ddg_general_parser import DDGGeneralParser


class DDGAdsParser(DDGGeneralParser):
    def __init__(self, *args):
        """ parses ad component
        """
        super().__init__(*args)

    def parse(self):
        return [self.parse_ad(i, ad) for i, ad in enumerate(self.cmpt.find("div", id="ads"))]

    def parse_ad(self, i, ad):
        return self.results | {
            "sub_rank": i,
            "url": self.get_url(ad),
            "title": self.get_title(),
        }

    def get_url(self, ad):
        return super().get_url(ad)

    def get_title(self):
        return super().get_title()