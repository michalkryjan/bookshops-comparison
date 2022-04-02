from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ProductModel import ProductModel
from scrappers.ScrapperHelper import ScrapperHelper


class Book5(ProductModel):
    def __init__(self, product_card_url: str):
        super().__init__()
        self._set_shop('Bookshop#5.pl')
        self._set_product_card_url(product_card_url)
        product_card_html = ScrapperHelper.parse_website_to_nested_data_structure(product_card_url)
        self._set_category(self.__extract_category_from_product_card(product_card_html))
        self._set_title(self.__extract_title_from_product_card(product_card_html))
        self._set_author(self.__extract_author_from_product_card(product_card_html))
        self._set_ean(self.__extract_ean_from_product_card(product_card_html))
        self._set_cover_price(self.__extract_cover_price_from_product_card(product_card_html))
        self._set_selling_price(self.__extract_selling_price_from_product_card(product_card_html))
        self._set_discount_amount_if_possible()
        self._set_time_to_send(self.__extract_time_to_send_from_product_card(product_card_html))

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_category_from_product_card(product_card_html: BeautifulSoup) -> list[str] | str:
        category = []
        breadcrumbs = product_card_html.find('section', {'class': 'breadcrumbs'}).find_all('a')
        for category_tag in breadcrumbs:
            category.append(category_tag.string.strip())
        return category[1:]

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_title_from_product_card(product_card_html: BeautifulSoup) -> str:
        return str(product_card_html.find('h1', {'class': 'title'}).contents[0]).strip()

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_author_from_product_card(product_card_html: BeautifulSoup) -> str:
        authors_links = product_card_html.find('h1', {'class': 'title'}).contents[1].find_all('a')
        final_author_value = authors_links[0].string.strip()
        if len(authors_links) > 1:
            for link in authors_links[1:]:
                final_author_value += f', {link.string.strip()}'
        return final_author_value

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_ean_from_product_card(product_card_html: BeautifulSoup) -> str:
        return product_card_html.find('strong', {'itemprop': 'sku'}).string.strip()

    @ErrorHandler.tag_extraction
    def __extract_cover_price_from_product_card(self, product_card_html: BeautifulSoup) -> float:
        price_with_currency = product_card_html.find('p', {'class': 'price'}).span.string.replace(',', '.')
        return self._convert_price_with_currency_to_float(price_with_currency)

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_selling_price_from_product_card(product_card_html: BeautifulSoup) -> float:
        return float(product_card_html.find('span', {'itemprop': 'price'}).attrs['content'])

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_time_to_send_from_product_card(product_card_html: BeautifulSoup) -> str:
        return product_card_html.find('span', {'class': 'buyNow'}).string.strip()
