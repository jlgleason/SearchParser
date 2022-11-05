import bs4.element
from bs4 import BeautifulSoup, SoupStrainer

# Treats every component as the same, extracts two types of info:
# what kind of component (ad or not)
# and what the url was (to classify the domain)
# find id=b_results and iterate through descendants
# API ad client: Fix US region, English sample, match type, ad position


def open_file(filename: str):
    try:
        with open(filename, mode="r") as infile:
            soup = BeautifulSoup(infile, "lxml")
            return soup
    except OSError:
        print("A file error occured")


# Appends new parsed components to components file
def save_data(newfile: str, parsed_data):
    with open(newfile, mode="a") as outfile:
        for each in parsed_data:
            outfile.write(str(each) + "\n")
    outfile.close()


# Saves prettified data
def save_pretty(newfile: str, soup):
    with open(newfile, mode="a") as outfile:
        for line in soup:
            outfile.write(str(line))
    outfile.close()


# Parses components in b_results tree and also searches for id tags
def parse_components(soup):
    parsed_data = []
    for cmpt in soup.find("ol", id="b_results"):
        parsed_data.append(cmpt["class"])
        if cmpt.has_attr("id"):
          parsed_data.append(cmpt["id"])
    return parsed_data


def main():
    # pretty_soup = open_file("bing_data.txt")
    # save_pretty("bing_output.txt", pretty_soup)
    soup = open_file("bing_data.txt")
    parsed_data = parse_components(soup)
    save_data("b_components.txt", parsed_data)


if __name__ == "__main__":
    main()
