from .general_parser import GeneralParser


class AdParser(GeneralParser):
    def __init__(self, *args):
        """ parses ad component
        """
        super().__init__(*args)

    def parse(self):
        return [self.parse_ad(i, ad) for i, ad in enumerate(self.cmpt.find("ul"))]

    def parse_ad(self, i, ad):
        return self.results | {
            "sub_rank": i,
            "url": self.get_url(ad),
            "title": self.get_title(ad),
        }

    def get_url(self, ad):
        return super().get_url(ad)
    
    def get_title(self, ad):
        title = ad.find("h2")
        if title:
            return title.get_text()
        else:
            return None
