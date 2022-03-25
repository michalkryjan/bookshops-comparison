import bs4
from bs4 import BeautifulSoup

from models.ProductModel import ProductModel
from scrappers.ScrapperHelper import ScrapperHelper


class Book4(ProductModel):
    def __init__(self, product_card_url: str):
        super().__init__()
        self._set_shop('Bookshop #4')
        self._set_product_card_url(product_card_url)
        product_card_html = ScrapperHelper.parse_website_to_nested_data_structure(product_card_url)
        self._set_category(self.__extract_category_from_product_card(product_card_html))
        self._set_title(self.__extract_title_from_product_card(product_card_html))
        self._set_author(self.__extract_author_from_product_card(product_card_html))
        self._set_ean(self.__extract_isbn_from_product_card(product_card_html))
        self._set_cover_price(self.__extract_cover_price_from_product_card(product_card_html))
        self._set_selling_price(self.__extract_selling_price_from_product_card(product_card_html))
        self._set_discount_amount_if_possible()
        self._set_time_to_send(self.__extract_time_to_send_from_product_card(product_card_html))

    def __extract_category_from_product_card(self, product_card_html: BeautifulSoup) -> list[str]:
        try:
            full_category = []
            breadcrumbs = product_card_html.find('ul', {'class': 'breadcrumbs-top'}).find_all('span', {'itemprop': 'name'})
            for category_name in breadcrumbs:
                full_category.append(category_name.string.strip())
            full_category.pop()  # removed product title
            return full_category
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __extract_title_from_product_card(self, product_hard_html: BeautifulSoup) -> str:
        try:
            return product_hard_html.find('h1', {'class': 'title'}).contents[0].strip()
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __extract_author_from_product_card(self, product_card_html: BeautifulSoup) -> str:
        try:
            return str(product_card_html.find('div', {'class': 'author'}).a.string).strip()
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __extract_isbn_from_product_card(self, product_card_html: BeautifulSoup) -> str:
        try:
            for li in product_card_html.find('div', {'id': 'product-details', 'class': 'details-list'}).ul.contents:
                if 'ISBN:' in str(li):
                    return li.contents[3].string.strip()
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __extract_selling_price_from_product_card(self, product_card_html: BeautifulSoup) -> float:
        try:
            price_box_container = product_card_html.find('div', {'class': 'price-box'})
            price_with_currency = price_box_container.find('span', {'class': 'current-price'}).string.strip().replace(',', '.')
            return self._convert_price_with_currency_to_float(price_with_currency)
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __extract_cover_price_from_product_card(self, product_card_html: BeautifulSoup) -> float:
        try:
            price_box_container = product_card_html.find('div', {'class': 'price-box'})
            price_with_currency = price_box_container.find('span', {'class': 'old-price'}).string.strip().replace(',', '.')
            return self._convert_price_with_currency_to_float(price_with_currency)
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __extract_time_to_send_from_product_card(self, product_card_html):
        try:
            sidebar_box_shipment = product_card_html.find('div', {'class': 'sidebar-box-shipment'})
            if isinstance(sidebar_box_shipment, bs4.element.Tag):
                return sidebar_box_shipment.find('span', {'class': 'shipping-time-label'}).string.strip()
            else:
                multi_sidebar_box = product_card_html.find('div', {'class': 'multi-sidebar-box'})
                date_of_availability = multi_sidebar_box.find('div', {'class': 'hide-time-counter-preview'}).string.strip()
                return 'Dostępny od: ' + date_of_availability
        except (AttributeError, TypeError):
            return self._value_not_found_fallback
