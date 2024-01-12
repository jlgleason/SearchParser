from .general_parser import GeneralParser


class AdParser(GeneralParser):
    def __init__(self, *args):
        """parses ad component from DDG SERP"""
        super().__init__(*args)

    def parse(self):
        self.results = super().parse()[0]
        self.results["cite"] = self.get_cite()
        return [self.results]

    def get_cite(self):
        attr = self.cmpt.find("a", attrs={"data-testid": "result-extras-url-link"})
        if attr:
            return attr.get_text()
        else:
            return None
