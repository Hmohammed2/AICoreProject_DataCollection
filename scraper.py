import requests
from bs4 import BeautifulSoup
import pandas as pd
from dataclasses import dataclass, field
from typing import List


@dataclass
class Data:
    Title: List[str] = field(default_factory=list)


class Scraper:

    url = "https://steamplayercount.com/popular"

    def __init__(self, response=None, get_url=url, page_number: int = 1):
        self.response = self.get_status if response is None else response
        self.get_url = get_url
        self.page_number = page_number

    def get_status(self):
        try:
            r = requests.get(self.pagination(self.page_number))
            return r
        except requests.exceptions.Timeout:
            print("Session Timeout")
            # Maybe set up for a retry, or continue in a retry loop
        except requests.exceptions.TooManyRedirects:
            print("Url is bad try a different one")
            # Tell the user their URL was bad and try a different one
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            raise SystemExit(e)

    def return_soup(self):
        # return soup object
        request = self.get_status()
        soup = BeautifulSoup(request.text, "html.parser")
        return soup

    def print_html(self):
        # prints the html in a more readable format
        soup = self.return_soup()
        return soup.prettify()

    def pagination(self, page_num:int):
        return f"{self.get_url}?page={page_num}"

    def extract_into_list(self, tag=str, class_str=None, index=None, soup=None):
        empty_list = []

        soup = self.return_soup() if soup is None else soup

        all_tags = soup.find_all(tag, class_=class_str)

        if not isinstance(soup, BeautifulSoup):
            raise TypeError
        else:

            if index is None:
                for container in all_tags:
                    name = container.text
                    empty_list.append(name)
            else:
                for container in all_tags[index]:
                    name = container.text
                    empty_list.append(name)

        return empty_list


if __name__ == "__main__":
    page_counter = 1
    scraper = Scraper()
    while True:
        try:
            page_counter += 1
            print(scraper.extract_into_list("a", "app-link"))
        except Exception as ex:
            print(ex)
            print("probably last page:", page_counter)
            break


