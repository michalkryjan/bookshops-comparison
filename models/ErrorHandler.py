from requests.exceptions import ConnectionError, MissingSchema


class ErrorHandler:
    @staticmethod
    def tag_extraction(extraction_method: callable):
        def wrapper(*args, **kwargs):
            try:
                return extraction_method(*args, **kwargs)
            except (AttributeError, TypeError, IndexError):
                return None
        return wrapper

    @staticmethod
    def return_none_if_any_argument_is_none(method: callable):
        def wrapper(*args, **kwargs):
            for arg in args:
                if arg is None:
                    return None
            for kwarg in kwargs:
                if kwarg is None:
                    return None
            return method(*args, **kwargs)
        return wrapper

    @staticmethod
    def website_parsing_request(method):
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except (ConnectionError, MissingSchema):
                print(f'ERROR while parsing {args[0]} to BeautifulSoup4 object!')
                return None
        return wrapper
