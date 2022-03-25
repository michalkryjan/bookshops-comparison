from bs4 import BeautifulSoup, Tag

from models.ProductModel import ProductModel
from scrappers.ScrapperHelper import ScrapperHelper


class Book3(ProductModel):
    def __init__(self, product_card_url: str):
        super().__init__()
        self._set_shop('Bookshop #3')
        self._set_product_card_url(product_card_url)
        product_card_html = ScrapperHelper.parse_website_to_nested_data_structure(product_card_url)
        atc_btn = self.__find_atc_btn_on_product_card(product_card_html)
        self._set_category(self.__try_to_extract_category_from_atc_btn(atc_btn))
        self._set_title(self.__try_to_extract_value_from_atc_btn(atc_btn, 'data-analytics-name'))
        self._set_author(self.__try_to_extract_value_from_atc_btn(atc_btn, 'data-analytics-brand'))
        self._set_cover_price(float(self.__try_to_extract_value_from_atc_btn(atc_btn, 'data-price')))
        self._set_selling_price(float(self.__try_to_extract_value_from_atc_btn(atc_btn, 'data-promotional-price')))
        self._set_discount_amount_if_possible()
        self._set_time_to_send(self.__extract_time_to_send_from_product_card(product_card_html))

    def __find_atc_btn_on_product_card(self, product_card_html: BeautifulSoup) -> BeautifulSoup:
        try:
            return product_card_html.find('button', {'data-title': 'Dodano do koszyka'})
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __try_to_extract_category_from_atc_btn(self, atc_btn: BeautifulSoup) -> list[str]:
        try:
            category = self.__try_to_extract_value_from_atc_btn(atc_btn, 'data-analytics-category')
            if category != self._value_not_found_fallback:
                if '/' in category:
                    return category.split('/')
                else:
                    return [category]
            else:
                return self._value_not_found_fallback
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __try_to_extract_value_from_atc_btn(self, atc_btn: BeautifulSoup, prop_name: str) -> str:
        try:
            if prop_name in atc_btn.attrs.keys():
                return atc_btn.attrs[prop_name]
            else:
                return self._value_not_found_fallback
        except (AttributeError, TypeError):
            return self._value_not_found_fallback

    def __extract_time_to_send_from_product_card(self, product_card_html: BeautifulSoup) -> str:
        try:
            availability_tag = product_card_html.find('div', {'data-ta': 'availability-info'})
            if isinstance(availability_tag.div, Tag):
                return availability_tag.div.string.replace('\n', '').strip()
            else:
                return availability_tag.string.replace('\n', ' ').strip()
        except (AttributeError, TypeError):
            return self._value_not_found_fallback
