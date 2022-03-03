import datetime


class ProductModel:
    def __init__(self):
        self.__shop = None
        self.__category = None
        self.__title = None
        self.__author = None
        self.__ean = None
        self.__cover_price = None
        self.__selling_price = None
        self.__discount_amount = None
        self.__time_to_send = None
        self.__stock_level = None
        self.__product_card_url = None
        self.__comment = None
        self._value_not_provided_fallback = 'Nie podano'
        self._value_not_found_fallback = 'Nie znaleziono'
        self._empty_stock_fallback = 'Brak w magazynie'

    def _set_shop(self, value: str):
        self.__shop = value

    def _set_category(self, value: list[str]):
        self.__category = '/'.join(value)

    def _set_title(self, value: str):
        self.__title = value

    def _set_author(self, value: str):
        self.__author = value

    def _set_ean(self, value: str):
        self.__ean = value.replace('-', '')

    def _set_cover_price(self, value: float):
        self.__cover_price = value

    def _set_selling_price(self, value: float):
        self.__selling_price = value

    def _set_discount_amount_if_possible(self):
        if isinstance(self.__cover_price, float) and isinstance(self.__selling_price, float):
            self.__discount_amount = round(self.__cover_price - self.__selling_price, 2)
        else:
            self.__discount_amount = self._value_not_found_fallback

    def _set_time_to_send(self, value: str):
        self.__time_to_send = value

    def _set_stock_level(self, value: str):
        self.__stock_level = value

    def _set_product_card_url(self, value: str):
        self.__product_card_url = value

    def set_comment(self, value: str):
        self.__comment = value

    def get_link_to_product_card(self):
        return self.__product_card_url

    def get_full_data(self) -> dict:
        return {
            'Data dodania': str(datetime.date.today().strftime('%d.%m.%Y')),
            'Sklep': self.__convert_to_fallback_value_if_none(self.__shop),
            'Kategoria w sklepie': self.__convert_to_fallback_value_if_none(self.__category),
            'Tytuł': self.__convert_to_fallback_value_if_none(self.__title),
            'Autor': self.__convert_to_fallback_value_if_none(self.__author),
            'EAN': self.__convert_to_fallback_value_if_none(self.__ean),
            'Cena okładkowa': self.__convert_to_fallback_value_if_none(self.__cover_price),
            'Cena sprzedaży': self.__convert_to_fallback_value_if_none(self.__selling_price),
            'Rabat od ceny okładkowej': self.__convert_to_fallback_value_if_none(self.__discount_amount),
            'Czas wysyłki': self.__convert_to_fallback_value_if_none(self.__time_to_send),
            'Liczba w magazynie': self.__convert_to_fallback_value_if_none(self.__stock_level),
            'Link do sklepu': self.__convert_to_fallback_value_if_none(self.__product_card_url),
            'Komentarz': self.__convert_to_fallback_value_if_none(self.__comment),
        }

    def __convert_to_fallback_value_if_none(self, value):
        if value is None:
            return self._value_not_provided_fallback
        else:
            return value

    @staticmethod
    def _convert_price_with_currency_to_float(price_with_currency: str) -> float:
        return float(price_with_currency[0:(price_with_currency.index('.') + 3)])
