from bs4 import BeautifulSoup

from models.ScrapperModel import ScrapperModel
from scrappers.ScrapperHelper import ScrapperHelper
from scrappers.bookshop1.Book1 import Book1


class Bookshop1HomepageScrapper(ScrapperModel):
    def __init__(self):
        super().__init__()
        self._set_full_homepage_html(ScrapperHelper.parse_website_to_nested_data_structure('HERE GOES BOOKSHOP #1 URL'))
        self._set_books(self.__create_books_from_homepage())
        print('bookshop #1 scrapped')

    def __create_books_from_homepage(self) -> list[Book1]:
        recommended_books_html = self.__extract_recommended_books_html_from_homepage()
        bestselling_books_html = self.__extract_bestselling_books_html_from_homepage()
        recommended_books = self.__convert_books_html_to_objects(recommended_books_html, 'Polecane')
        bestselling_books = self.__convert_books_html_to_objects(bestselling_books_html, 'Bestseller')
        return [*recommended_books, *bestselling_books]

    def __extract_recommended_books_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.find_all('div', {'class': 'col-12 col-sm-12 col-lg-6 p-3'})

    def __extract_bestselling_books_html_from_homepage(self) -> list[BeautifulSoup]:
        return self._full_homepage_html.find_all('div', {'class': 'col-12 col-lg-6'})

    def __convert_books_html_to_objects(self, books_html: list[BeautifulSoup], comment: str):
        books = []
        for book_html in books_html:
            product_card_url = self.__extract_link_from_book_html(book_html)
            book = Book1(product_card_url)
            book.set_comment(comment)
            books.append(book)
        return books

    @staticmethod
    def __extract_link_from_book_html(book_html: BeautifulSoup) -> str:
        return  book_html.find_all('a')[1].attrs['href']


def print_products_from_homepage():
    bookshop1 = Bookshop1HomepageScrapper()
    for product in bookshop1.get_books_data():
        print(product)


if __name__ == '__main__':
    print_products_from_homepage()
