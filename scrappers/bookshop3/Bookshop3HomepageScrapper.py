from bs4 import BeautifulSoup

from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop3.Book3 import Book3


class Bookshop3HomepageScrapper(ScrapperModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP #3 URL'))
        self._set_books(self.__create_books_from_homepage())
        print('bookshop #3 scrapped')

    def __create_books_from_homepage(self) -> list[Book3]:
        books = []
        products_wrappers_with_titles = self.__extract_products_wrappers_with_titles()
        for wrapper_title in products_wrappers_with_titles.keys():
            books_html = self.__extract_books_html_from_product_wrapper(products_wrappers_with_titles[wrapper_title])
            for book_html in books_html:
                books.append(self.__create_single_book(book_html, wrapper_title))
        return books

    def __create_single_book(self, book_html: BeautifulSoup, comment: str) -> Book3:
        product_card_url = self.__extract_link_from_book_html(book_html)
        book = Book3(product_card_url)
        book.set_comment(comment)
        return book

    def __extract_products_wrappers_with_titles(self) -> dict:
        products_wrappers = self._full_homepage_html.find_all('section', {'class': 'whiteBox'})
        products_wrappers_with_titles = {}
        for item in products_wrappers[:-2]:
            title = item.find('h2', {'class': 'whiteBox__title'}).string.strip()
            products_wrappers_with_titles[title] = item
        return products_wrappers_with_titles

    @staticmethod
    def __extract_books_html_from_product_wrapper(product_wrapper: BeautifulSoup) -> list[BeautifulSoup]:
        return product_wrapper.find_all('div', {'class': 'productsList__product'})[:-1]

    @staticmethod
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return book_html.find('a', {'class': 'seoTitle'}).attrs['href']


def print_products_from_homepage():
    bookshop3 = Bookshop3HomepageScrapper()
    for product in bookshop3.get_books_data():
        print(product)


if __name__ == '__main__':
    print_products_from_homepage()
