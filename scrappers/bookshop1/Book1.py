from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ProductModel import ProductModel
from scrappers.ScrapperHelper import ScrapperHelper


class Book1(ProductModel):
    def __init__(self, product_card_url: str):
        super().__init__()
        self._set_shop('Bookshop1.pl')
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
        self._set_stock_level(self.__extract_stock_level_from_product_card(product_card_html))

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_category_from_product_card(product_card_html: BeautifulSoup) -> list[str]:
        return product_card_html.find('span', {'itemprop': 'category'}).attrs['content'].split(' > ')[1:]

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_title_from_product_card(product_card_html: BeautifulSoup) -> str:
        return product_card_html.find('span', {'itemprop': 'name'}).string.strip()

    @ErrorHandler.tag_extraction
    def __extract_author_from_product_card(self, product_card_html: BeautifulSoup) -> str:
        for item in self.__extract_product_props_list(product_card_html):
            if 'Autor' in str(item):
                return item.contents[1].a.string.strip()

    @ErrorHandler.tag_extraction
    def __extract_ean_from_product_card(self, product_card_html: BeautifulSoup) -> str:
        for item in self.__extract_product_props_list(product_card_html):
            if 'EAN' in str(item):
                return item.contents[1].span.b.string.strip()

    @ErrorHandler.tag_extraction
    def __extract_product_props_list(self, product_card_html: BeautifulSoup) -> BeautifulSoup:
        return self.__extract_main_product_info_div(product_card_html).table.contents

    @ErrorHandler.tag_extraction
    def __extract_main_product_info_div(self, product_card_html: BeautifulSoup) -> BeautifulSoup:
        return product_card_html.find('div', {'class': 'col-12 col-lg-8 order-2 order-lg-1 p-3'})

    @ErrorHandler.tag_extraction
    def __extract_selling_price_from_product_card(self, product_card_html: BeautifulSoup) -> float:
        schema_offer_tag = self.__extract_schema_offer_tag_from_product_card(product_card_html)
        return float(schema_offer_tag.find('meta', {'itemprop': 'price'}).attrs['content'].strip())

    @ErrorHandler.tag_extraction
    def __extract_schema_offer_tag_from_product_card(self, product_card_html: BeautifulSoup):
        main_product_info_div = self.__extract_main_product_info_div(product_card_html)
        return main_product_info_div.find('span', {'itemprop': 'offers', 'itemtype': 'https://schema.org/Offer'})

    @ErrorHandler.tag_extraction
    def __extract_cover_price_from_product_card(self, product_card_html: BeautifulSoup) -> float:
        for item in self.__extract_product_props_list(product_card_html):
            if 'Cena rynkowa' in str(item):
                price_with_currency = item.contents[1].font.b.string.strip().replace(',', '.')
                return self._convert_price_with_currency_to_float(price_with_currency)

    @ErrorHandler.tag_extraction
    def __extract_time_to_send_from_product_card(self, product_card_html: BeautifulSoup) -> str:
        single_shipping_info_line = self.__extract_single_shipping_info_line_from_product_card(product_card_html)
        if single_shipping_info_line is not None and not isinstance(single_shipping_info_line, str):
            time_to_send = single_shipping_info_line.contents[1].font.contents[0]
            return self.__remove_redundant_characters(time_to_send)

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_single_shipping_info_line_from_product_card(product_card_html: BeautifulSoup) -> BeautifulSoup:
        shipping_info_container = product_card_html.find('div', {'class': 'col-12 mb-3'})
        return shipping_info_container.table.tr.td.table.contents[1]

    @ErrorHandler.tag_extraction
    def __extract_stock_level_from_product_card(self, product_card_html: BeautifulSoup) -> str:
        main_product_info_div = self.__extract_main_product_info_div(product_card_html)
        meta_availability_tag = main_product_info_div.find('meta', {'itemprop': 'availability'})
        if meta_availability_tag.attrs['content'] == 'InStock':
            if meta_availability_tag.tr is not None:
                stock_level = meta_availability_tag.tr.contents[1].font.contents[1]
                return self.__remove_redundant_characters(stock_level)
            else:
                return 'W magazynie'
        else:
            return self._empty_stock_fallback

    @staticmethod
    def __remove_redundant_characters(text: str) -> str:
        return text.replace('(', '').replace(')', '').strip()
