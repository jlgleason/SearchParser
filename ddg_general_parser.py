import bs4


class DDGGeneralParser:

    def __init__(self, cmpt: bs4.element.Tag, cmpt_type: str):
        """
        Parses general component from DDG SERP
        :param cmpt: Beautiful Soup Tag element
        :param cmpt_type: (str) component type 
        """
        self.cmpt = cmpt
        self.results = {"type": cmpt_type}

    def parse(self):
        self.results["sub_rank"] = 0
        self.results["url"] = self.get_url(self.cmpt)
        self.results["title"] = self.get_title()
        return [self.results]

    def get_url(self, cmpt):
        attr = cmpt.find("h2", class_="LnpumSThxEWMIsDdAT17 CXMyPcQ6nDv47DKFeywM")
        if attr:
            return attr.find("a", class_="eVNpHGjtxRBq_gLOfGDr LQNqh2U1kzYxREs65IJu").get("href")
        else:
            return None

    def get_title(self):
        title = soup.body.find("span", class_="EKtkFWMYpwzMKOYr0GYm LQVY1Jpkk8nyJ6HBWKAk")
        if title:
            return title.get_text()
        else:
            return None