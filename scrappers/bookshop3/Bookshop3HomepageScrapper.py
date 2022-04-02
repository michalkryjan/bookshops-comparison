from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop3.Book3 import Book3


class Bookshop3HomepageScrapper(ScrapperModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP #3 URL'))
        if self._full_homepage_html is not None:
            self._set_books(self.__create_books_from_homepage())
            print('Bookshop#3.pl scrapped')

    def __create_books_from_homepage(self) -> list[Book3]:
        books = []
        products_wrappers_with_titles = self.__extract_products_wrappers_with_titles()
        for wrapper_title in products_wrappers_with_titles.keys():
            books_html = self.__extract_books_html_from_product_wrapper(products_wrappers_with_titles[wrapper_title])
            books = ScrapperHelper.merge_not_none_lists(books, self.__create_objects_from_books_html(books_html, wrapper_title))
        return books

    @ErrorHandler.tag_extraction
    def __extract_products_wrappers_with_titles(self) -> dict:
        products_wrappers = self._full_homepage_html.find_all('section', {'class': 'whiteBox'})
        products_wrappers_with_titles = {}
        for item in products_wrappers[:-2]:
            title = item.find('h2', {'class': 'whiteBox__title'}).string.strip()
            products_wrappers_with_titles[title] = item
        return products_wrappers_with_titles

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_books_html_from_product_wrapper(product_wrapper: BeautifulSoup) -> list[BeautifulSoup]:
        return product_wrapper.find_all('div', {'class': 'productsList__product'})[:-1]

    @ErrorHandler.return_none_if_any_argument_is_none
    def __create_objects_from_books_html(self, books_html: list[BeautifulSoup], comment: str) -> list[Book3]:
        books = []
        for book_html in books_html:
            product_card_url = self.__extract_link_from_book_html(book_html)
            book = Book3(product_card_url)
            book.set_comment(comment)
            books.append(book)
        return books

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return 'HERE GOES BOOKSHOP#3 CORE URL' + book_html.find('a', {'class': 'seoTitle'}).attrs['href']


if __name__ == '__main__':
    ScrapperHelper.print_products_from_homepage(Bookshop3HomepageScrapper())

