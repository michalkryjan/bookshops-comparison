from bs4 import BeautifulSoup

from models.ProductModel import ProductModel


class ScrapperModel:
    def __init__(self):
        self._full_homepage_html = None
        self._books = None

    def _set_full_homepage_html(self, value: BeautifulSoup):
        self._full_homepage_html = value

    def _set_books(self, books_list: list[ProductModel]):
        self._books = books_list

    def get_books_data(self) -> list[dict]:
        books_data = list()
        for book in self._books:
            books_data.append(book.get_full_data())
        return books_data
