from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop5.Book5 import Book5


class Bookshop5HomepageScrapper(ScrapperModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP#5 URL'))
        if self._full_homepage_html is not None:
            self._set_books(self.__create_books_from_homepage())
            print('Bookshop#5.pl scrapped')

    def __create_books_from_homepage(self) -> list[Book5]:
        books = []
        sliders_html = self.__extract_sliders_html_from_homepage()
        if sliders_html is not None:
            for slider_html in sliders_html:
                comment = self.__extract_slider_title(slider_html)
                books_html = self.__extract_books_html_from_slider(slider_html)
                books = ScrapperHelper.merge_not_none_lists(books, self.__convert_books_html_to_objects(books_html, comment))
        return books

    @ErrorHandler.tag_extraction
    def __extract_sliders_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.find_all('section', {'class': 'booksSliderMain'})

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_slider_title(slider_html: BeautifulSoup) -> str:
        return slider_html.find('h2', {'class': 'mainTitle'}).string.strip()

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_books_html_from_slider(slider_html: BeautifulSoup) -> list[BeautifulSoup]:
        return slider_html.find_all('div', {'class': 'imgBox'})

    @ErrorHandler.return_none_if_any_argument_is_none
    def __convert_books_html_to_objects(self, books_html: list[BeautifulSoup], comment: str) -> list[Book5]:
        books = []
        for book_html in books_html:
            book = Book5(self.__extract_link_from_book_html(book_html))
            book.set_comment(comment)
            books.append(book)
        return books

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return book_html.find('p', {'class': 'title'}).a.attrs['href']


if __name__ == '__main__':
    ScrapperHelper.print_products_from_homepage(Bookshop5HomepageScrapper())
