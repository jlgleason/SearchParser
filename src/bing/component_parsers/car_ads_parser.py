from .general_parser import GeneralParser


class CarAdsParser(GeneralParser):
    def __init__(self, *args):
        """parses shopping ad component"""
        super().__init__(*args)
        self.results["type"] = "shopping_ads"

    def parse(self):
        titles = self.cmpt.find_all("div", class_="title")
        urls = self.cmpt.find_all("a", class_="")
        return [
            self.parse_shopping_ad(i, title, url)
            for i, (title, url) in enumerate(zip(titles, urls))
        ]

    def parse_shopping_ad(self, i, title, url):
        return self.results | {
            "sub_rank": i,
            "url": self.get_url(url),
            "title": self.get_title(title),
        }

    def get_url(self, url):
        return url.get("href")

    def get_title(self, title):
        return title.get_text()

