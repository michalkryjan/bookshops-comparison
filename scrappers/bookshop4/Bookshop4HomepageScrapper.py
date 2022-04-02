from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ProductModel import ProductModel
from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop4.Book4 import Book4


class Bookshop4HomepageScrapper(ScrapperModel, ProductModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP#4 URL'))
        if self._full_homepage_html is not None:
            books = self.__create_objects_from_books_html(self.extract_books_html_from_homepage())
            self._set_books(books if books is not None else [])
            print('Bookshop#4.pl scrapped')

    @ErrorHandler.return_none_if_any_argument_is_none
    def __create_objects_from_books_html(self, books_html: list[BeautifulSoup]) -> list[Book4]:
        books = []
        for book_html in books_html:
            product_card_url = self.__extract_link_from_book_html(book_html)
            books.append(Book4(product_card_url))
        return books

    @ErrorHandler.tag_extraction
    def extract_books_html_from_homepage(self) -> list[BeautifulSoup]:
        books_html = []
        for item in self.extract_all_products_html_from_homepage():
            if 'onclick' in item.a.attrs:
                ga_product_data = item.a.attrs['onclick']
                if 'Książki' in ga_product_data:
                    books_html.append(item)
        return books_html

    @ErrorHandler.tag_extraction
    def extract_all_products_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.find_all('div', class_='info-box')

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return book_html.find('a', {'class': 'title'}).attrs['href'].strip()


if __name__ == '__main__':
    ScrapperHelper.print_products_from_homepage(Bookshop4HomepageScrapper())
