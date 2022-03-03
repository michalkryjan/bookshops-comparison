from bs4 import BeautifulSoup

from models.ProductModel import ProductModel
from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop4.Book4 import Book4


class Bookshop4HomepageScrapper(ScrapperModel, ProductModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP #4 URL'))
        self._set_books(self.__create_books_from_homepage())
        print('bookshop #4 scrapped')

    def __create_books_from_homepage(self) -> list[Book4]:
        books = []
        for book_html in self.extract_books_html_from_homepage():
            product_card_url = self.__extract_link_from_book_html(book_html)
            books.append(Book4(product_card_url))
        return books

    def extract_books_html_from_homepage(self) -> list[BeautifulSoup]:
        books_html = []
        for item in self.extract_all_products_html_from_homepage():
            if 'onclick' in item.a.attrs:
                ga_product_data = item.a.attrs['onclick']
                if 'Książki' in ga_product_data:
                    books_html.append(item)
        return books_html

    def extract_all_products_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.find_all('div', class_='info-box')

    @staticmethod
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return book_html.find('a', {'class': 'title'}).attrs['href'].strip()


def print_products_from_homepage():
    bookshop4 = Bookshop4HomepageScrapper()
    for product in bookshop4.get_books_data():
        print(product)


if __name__ == '__main__':
    print_products_from_homepage()
