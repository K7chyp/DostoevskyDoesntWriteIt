from urllib.request import urlopen
from bs4 import BeautifulSoup

UTF_8: str = "utf8"
MAIN_URL: str = "https://knijky.ru"


class AuthorPageParser:
    def __init__(self):
        self.request_ = urlopen(MAIN_URL + "/authors/fedor-dostoevskiy/")
        self.html: str = self.request_.read().decode(UTF_8)
        self.soup = BeautifulSoup(self.html, "lxml")
        self.author_page_content_parser()

    def find_information_from_field_content(self, information_from_page) -> str:
        return information_from_page.find("span", {"class": "field-content"})

    def author_page_content_parser(self) -> None:
        self.information: dict = {
            part_of_page.find("a").get("href"): part_of_page.find("a").text
            for part_of_page in self.soup.find_all(
                "div", {"class": "views-field views-field-title"}
            )
        }


print(AuthorPageParser().information)