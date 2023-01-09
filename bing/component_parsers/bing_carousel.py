from .general_parser import GeneralParser


class ShoppingAdsParser(GeneralParser):
    def __init__(self, *args):
        """parses shopping ad component"""
        super().__init__(*args)

    def parse(self):
        titles = self.cmpt.find_all("span", class_="b_adsTrunTx")
        urls = self.cmpt.find_all("a", class_='')
        return [
            self.parse_shopping_ad(i, ad)
            for i, ad in zip(titles, urls)
        ]

    def parse_shopping_ad(self, i, ad):
        return self.results | {
                "sub_rank": i,
                "url" : self.get_url(ad),
                "title": self.get_title(ad),
        }

    def get_url(self, ad):
        return ad.get("href")


    def get_title(self, ad):
        return '|'.join([t.text for t in ad])

