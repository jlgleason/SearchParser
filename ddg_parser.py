from bs4 import BeautifulSoup, SoupStrainer

import parser

# Treats every component as the same, extracts two types of info:
# what kind of component (ad or not)
# and what the url was (to classify the domain)
# find id=b_results and iterate through descendants
# API ad client: Fix US region, English sample, match type, ad position


# Parses components in results--main tree and also searches for id tags
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



def main():
    # Open SERPs file and make soup
    soup = parser.open_file("/Users/alicekoeninger/PycharmProjects/ddg_searcher/ddg_data.txt")
    # Parse components
    parsed_data = parse_components(soup)
    # Write parsed data to file 
    parser.save_data("ddg_components.txt", parsed_data)


if __name__ == "__main__":
    main()
