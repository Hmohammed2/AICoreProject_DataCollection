import requests
from bs4 import BeautifulSoup
import pandas as pd
from dataclasses import dataclass, field
from typing import List
import re


@dataclass
class Data:
    Product_name: List[str] = field(default_factory=list)
    Price: List[str] = field(default_factory=list)
    Summary: List[str] = field(default_factory=list)


class Scraper:

    default_url = "https://www.arcadeworlduk.com/"

    def __init__(self, response=None, get_url=default_url, **kwargs):
        self.response = self.get_status if response is None else response
        self.get_url = get_url
        self.search_query = input('Enter product name: ')

    def get_status(self, page_number=None):
        try:
            r = requests.get(self.search_product()) if page_number is None else requests.get(self.pagination(page_number))
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

    def search_product(self):
        return f"{self.get_url}search.php?search_query={self.search_query}&section=product"

    def return_soup(self, page_number=None):
        # return soup object
        request = self.get_status() if page_number is None else self.get_status(page_number)
        soup = BeautifulSoup(request.text, "html.parser")
        return soup

    def print_html(self):
        # prints the html in a more readable format
        soup = self.return_soup()
        return soup.prettify()

    def pagination(self, page_num: int):
        return f"{self.get_url}search.php?page={page_num}&section=product&search_query={self.search_query}"

    def extract_into_list(self, tag: str, class_str=None, href=False, index=None, soup=None, attrs=None):
        empty_list = []

        soup = self.return_soup() if soup is None else soup

        all_tags = soup.find_all(tag, class_=class_str, href=href, attrs=attrs)

        if not isinstance(soup, BeautifulSoup):
            # checks if object is of bs4 type, in case an argument was passed for the "soup" parameter
            raise TypeError
        else:
            if index is None:
                for container in all_tags:
                    name = container.text
                    if re.search(r"\w+[\s]|[£]\d+", name):
                        empty_list.append(name)
            else:
                for container in all_tags[index]:
                    name = container.text
                    empty_list.append(name)

        return empty_list


class ToCsv:
    pass


def main(iterate=False):

    page_counter = 1
    scraper = Scraper()
    if iterate is True:
        while True:
            try:
                page_counter += 1
                data = scraper.return_soup(page_counter)
                print(scraper.extract_into_list(tag="a", href=True, soup=data, attrs={"data-event-type": True}))
                print(scraper.extract_into_list(tag="span", class_str="price", soup=data))
                print(scraper.extract_into_list(tag="p", class_str="card-summary", soup=data))
            except Exception as ex:
                print(ex)
                print("probably last page:", page_counter)
                break
    else:
        try:
            data = scraper.return_soup(page_counter)
            print(scraper.extract_into_list(tag="a", href=True, soup=data, attrs={"data-event-type": True}))
            print(scraper.extract_into_list(tag="span", class_str="price", soup=data, attrs={"data-product-price-with"
                                                                                             "-tax": True}))
            print(scraper.extract_into_list(tag="p", class_str="card-summary", soup=data))
        except Exception as ex:
            print(ex)


if __name__ == "__main__":
    main(True)
