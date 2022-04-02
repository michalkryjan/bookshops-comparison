from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop2.Book2 import Book2


class Bookshop2HomepageScrapper(ScrapperModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP#2 URL'))
        if self._full_homepage_html is not None:
            books = self.__create_objects_from_books_html(self.__extract_books_html_from_homepage())
            self._set_books(books if books is not None else [])
            print('bookshop#2.pl scrapped')

    @ErrorHandler.return_none_if_any_argument_is_none
    def __create_objects_from_books_html(self, books_html: list[BeautifulSoup]) -> list[Book2]:
        books = []
        for book_html in books_html:
            product_card_url = self.__extract_link_from_book_html(book_html)
            books.append(Book2(product_card_url))
        return books

    @ErrorHandler.tag_extraction
    def __extract_books_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.findAll(itemprop="item")

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_link_from_book_html(book_html: BeautifulSoup):
        return book_html.find('h2', {'class': 'product-title'}).a.attrs['href'].strip()


if __name__ == '__main__':
    ScrapperHelper.print_products_from_homepage(Bookshop2HomepageScrapper())
