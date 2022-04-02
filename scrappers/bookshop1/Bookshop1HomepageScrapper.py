from bs4 import BeautifulSoup
from scrappers.bookshop1.Book1 import Book1

from models.ErrorHandler import ErrorHandler
from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper


class Bookshop1HomepageScrapper(ScrapperModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP#1 URL'))
        if self._full_homepage_html is not None:
            self._set_books(self.__create_books_from_homepage())
            print('bookshop1.pl scrapped')

    def __create_books_from_homepage(self) -> list[Book1]:
        recommended_books_html = self.__extract_recommended_books_html_from_homepage()
        bestselling_books_html = self.__extract_bestselling_books_html_from_homepage()
        recommended_books = self.__convert_books_html_to_objects(recommended_books_html, 'Polecane')
        bestselling_books = self.__convert_books_html_to_objects(bestselling_books_html, 'Bestseller')
        return ScrapperHelper.merge_not_none_lists(recommended_books, bestselling_books)

    @ErrorHandler.tag_extraction
    def __extract_recommended_books_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.find_all('div', {'class': 'col-12 col-sm-12 col-lg-6 p-3'})

    @ErrorHandler.tag_extraction
    def __extract_bestselling_books_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.find_all('div', {'class': 'col-12 col-lg-6'})

    @ErrorHandler.return_none_if_any_argument_is_none
    def __convert_books_html_to_objects(self, books_html: list[BeautifulSoup], comment: str):
        books = []
        for book_html in books_html:
            product_card_url = self.__extract_link_from_book_html(book_html)
            book = Book1(product_card_url)
            book.set_comment(comment)
            books.append(book)
        return books

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return 'HERE GOES BOOKSHOP#1 URL' + book_html.find_all('a')[1].attrs['href']


if __name__ == '__main__':
    ScrapperHelper.print_products_from_homepage(Bookshop1HomepageScrapper())
