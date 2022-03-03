from bs4 import BeautifulSoup

from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop2.Book2 import Book2


class Bookshop2HomepageScrapper(ScrapperModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP #2 URL'))
        self._set_books(self.__create_books_from_homepage())
        print('bookshop #2 scrapped')

    def __create_books_from_homepage(self) -> list[Book2]:
        books = []
        for book_html in self.__extract_books_html_from_homepage():
            product_card_url = self.__extract_link_from_book_html(book_html)
            books.append(Book2(product_card_url))
        return books

    def __extract_books_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.findAll(itemprop="item")

    @staticmethod
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return book_html.find('h2', {'class': 'product-title'}).a.attrs['href'].strip()


def print_products_from_homepage():
    bookshop2 = Bookshop2HomepageScrapper()
    for product in bookshop2.get_books_data():
        print(product)


if __name__ == '__main__':
    print_products_from_homepage()
