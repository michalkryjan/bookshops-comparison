import requests
from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ScrapperModel import ScrapperModel


class ScrapperHelper:
    @classmethod
    @ErrorHandler.website_parsing_request
    def parse_website_to_nested_data_structure(cls, url: str) -> BeautifulSoup:
        r = requests.get(url)
        return BeautifulSoup(r.text, 'html.parser')

    @staticmethod
    def print_products_from_homepage(homepage_scrapper: ScrapperModel):
        for product in homepage_scrapper.get_books_data():
            print(product)

    @staticmethod
    def merge_not_none_lists(*args):
        merged = []
        for arg in args:
            if isinstance(arg, list) and arg is not None:
                merged = [*merged, *arg]
        return merged
