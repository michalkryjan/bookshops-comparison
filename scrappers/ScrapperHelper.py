import requests
from bs4 import BeautifulSoup


class ScrapperHelper:
    @classmethod
    def parse_website_to_nested_data_structure(cls, url: str) -> BeautifulSoup:
        return BeautifulSoup(cls.__get_html_source_code(url), 'html.parser')

    @staticmethod
    def __get_html_source_code(url: str) -> str:
        r = requests.get(url)
        return r.text
