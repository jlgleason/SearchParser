from .general_parser import GeneralParser


class UnknownParser(GeneralParser):
    def __init__(self, *args):
        """ parses unknown component
        """
        super().__init__(*args)

    def parse(self):
        return [self.results | {"sub_rank": 0}]

