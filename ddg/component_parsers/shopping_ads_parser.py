from .general_parser import GeneralParser


class ShoppingAdsParser(GeneralParser):
    def __init__(self, *args):
        """parses shopping ad component"""
        super().__init__(*args)

    def parse(self):
        return [
            self.parse_shopping_ad(i, ad)
            for i, ad in enumerate(
                self.cmpt.find_all("a", class_="module--carousel__body__title")
            )
        ]

    def parse_shopping_ad(self, i, ad):
        return self.results | {
            "sub_rank": i,
            "url": self.get_url(ad),
            "title": self.get_title(ad),
        }

    def get_url(self, ad):
        return ad.get("href")

    def get_title(self, ad):
        return ad.text
