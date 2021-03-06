from bs4 import BeautifulSoup

from models.ErrorHandler import ErrorHandler
from models.ProductModel import ProductModel
from scrappers.ScrapperHelper import ScrapperHelper


class Book2(ProductModel):
    def __init__(self, product_card_url: str):
        super().__init__()
        self._set_shop('Bookshop#2.pl')
        self._set_product_card_url(product_card_url)
        product_card_html = ScrapperHelper.parse_website_to_nested_data_structure(product_card_url)
        self.__details_list = self.__extract_details_list_from_product_card(product_card_html)
        self._set_category(self.__extract_category_from_product_card(product_card_html))
        self._set_title(self.__extract_title())
        self._set_author(self.__extract_author())
        self._set_ean(self.__extract_isbn())
        self._set_selling_price(self.__extract_selling_price_from_product_card(product_card_html))
        self._set_cover_price(self.__extract_cover_price_from_product_card(product_card_html))
        self._set_discount_amount_if_possible()
        self._set_time_to_send(self.__extract_time_to_send_from_product_card(product_card_html))

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_details_list_from_product_card(product_card_html: BeautifulSoup):
        main_product_info_container = product_card_html.find_all('blockquote', {'class': 'size-12'})[1]
        params = []
        for item in str(main_product_info_container.p).replace('<p>', '').replace('</p>', '').split('<br clear="all"/>'):
            params.append(BeautifulSoup(item, 'html.parser'))
        return params

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_category_from_product_card(product_card_html: BeautifulSoup) -> list[str]:
        full_category = []
        breadcrumbs = product_card_html.find('div', {'id': 'breadcrumb'}).find_all('span', {'itemprop': 'name'})
        for category_name in breadcrumbs:
            full_category.append(category_name.string.strip())
        return full_category[1:-1]

    @ErrorHandler.tag_extraction
    def __extract_title(self) -> str:
        return self.__find_single_detail_value_by_name('Tytu??')

    @ErrorHandler.tag_extraction
    def __find_single_detail_value_by_name(self, param_name: str) -> str:
        for item in self.__details_list:
            if param_name in str(item.span):
                return str(item.strong.string).strip()

    @ErrorHandler.tag_extraction
    def __extract_author(self) -> str:
        return self.__find_single_detail_value_by_name('Autor')

    @ErrorHandler.tag_extraction
    def __extract_isbn(self) -> str:
        return self.__find_single_detail_value_by_name('ISBN')

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_selling_price_from_product_card(product_card_html: BeautifulSoup) -> float:
        return float(product_card_html.find('div', {'class': 'price'}).strong.contents[0].strip().replace(',', '.'))

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_cover_price_from_product_card(product_card_html: BeautifulSoup) -> float:
        return float(product_card_html.find('div', {'class': 'oldPirce'}).strong.contents[0].strip().replace(',', '.'))

    @staticmethod
    @ErrorHandler.tag_extraction
    def __extract_time_to_send_from_product_card(product_card_html: BeautifulSoup) -> str:
        return product_card_html.find('div', {'class': 'jbWysylka'}).span.string.strip().replace('Wysy??ka: ', '')
