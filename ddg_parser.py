from bs4 import BeautifulSoup, SoupStrainer

import parser


# Parses components in ads and links trees, also searches for id tags
def parse_components(soup):
    parsed_data = []
    head = soup.body
    for cmpt in head.find("div", id="ads"):
        parsed_data.append(cmpt["class"])
        for each in cmpt.children:
            if each.has_attr("class"):
                parsed_data.append(each["class"])
            elif each.has_attr("id"):
                parsed_data.append(each["id"])
    for cmpt in head.find("div", id="links"):
        parsed_data.append(cmpt["class"])
        for each in cmpt.children:
            if each.has_attr("class"):
                parsed_data.append(each["class"])
            elif each.has_attr("id"):
                parsed_data.append(each["id"])
    return parsed_data

# Finds url of result by finding h2 component with specific class in soup, then uses that to find the url
def get_url(soup):
    attr = soup.find("h2", class_="LnpumSThxEWMIsDdAT17 CXMyPcQ6nDv47DKFeywM")
    if attr:
        return attr.find("a", class_="eVNpHGjtxRBq_gLOfGDr LQNqh2U1kzYxREs65IJu").get("href")
    else:
        return None
# Finds title of result by searching for span component in soup and returning the text 
def get_title(soup):
    title = soup.body.find("span", class_="EKtkFWMYpwzMKOYr0GYm LQVY1Jpkk8nyJ6HBWKAk")
    if title:
        return title.get_text()
    else:
        return None


def main():
    # Open SERPs file and make soup
    soup = parser.open_file("/Users/alicekoeninger/PycharmProjects/ddg_searcher/ddg_data.txt")
    # Parse components
    parsed_data = parse_components(soup)

    # Write parsed data to file
    parser.save_data("/Users/alicekoeninger/PycharmProjects/ddg_searcher/ddg_components.txt", parsed_data)
    # Not sure where we want the output of these functions to go
    print(get_title(soup))
    print(get_url(soup))


if __name__ == "__main__":
    main()
