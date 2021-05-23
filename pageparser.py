from urllib.request import urlopen
from bs4 import BeautifulSoup
from re import findall
from tqdm import trange

UTF_8: str = "utf8"
MAIN_URL: str = "https://knijky.ru"
LAST_ELEMENT = -1


class PageBaseClass:
    def __init__(self, url):
        self.url = url
        self.request_ = urlopen(self.url)
        self.html: str = self.request_.read().decode(UTF_8)
        self.soup = BeautifulSoup(self.html, "lxml")


class PageHrefsParser(PageBaseClass):
    def __init__(self, url):
        super().__init__(url)
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
        self.last_page: int = max(
            int(value)
            for value in [
                findall(r"\d+", str(item))
                for item in self.soup.find_all("div", {"class": "item-list"})
            ][0]
        )


class AuthorHrefParser:
    def __init__(self, author_name):
        self.author_name: str = author_name
        self.author_page_name: str = MAIN_URL + "/authors/{}/".format(self.author_name)
        self.get_all_books_hrefs_for_parsing()

    def get_all_books_hrefs_for_parsing(self) -> None:
        last_page: int = PageHrefsParser(self.author_page_name).last_page
        self.output: dict = {}
        for page_number in range(last_page):
            current_href = self.author_page_name + "?page={}".format(page_number)
            information_from_current_page: dict = PageHrefsParser(
                current_href
            ).information
            self.output = {**information_from_current_page, **self.output}


class TextFromPageParser(PageBaseClass):
    def __init__(self, url):
        super().__init__(url)
        self.get_text_from_page()

    def get_text_from_page(self):
        self.text = " ".join(
            part_of_page.text.replace("\xa0", "")
            for part_of_page in self.soup.find_all("p")
        )


class GetBookText(PageBaseClass):
    def __init__(self, href):
        super().__init__(MAIN_URL + href)
        self.get_all_book_text()

    def get_last_page_number(self):
        self.last_page_number: int = int(
            [
                findall(r"\d+", str(value))
                for value in self.soup.find_all("div", {"class": "pager"})
            ][0][LAST_ELEMENT]
        )

    def get_all_book_text(self):
        self.get_last_page_number()
        self.book_text: str = ""
        for page_number in trange(1, self.last_page_number):
            self.book_text += TextFromPageParser(
                self.url + "?page={}".format(page_number)
            ).text


print(GetBookText("/books/idiot").book_text)
