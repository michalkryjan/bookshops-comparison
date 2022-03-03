from apscheduler.schedulers.blocking import BlockingScheduler
import logging
from scrappers.bookshop1.Bookshop1HomepageScrapper import Bookshop1HomepageScrapper
from scrappers.bookshop2.Bookshop2HomepageScrapper import Bookshop2HomepageScrapper
from scrappers.bookshop3.Bookshop3HomepageScrapper import Bookshop3HomepageScrapper
from scrappers.bookshop4.Bookshop4HomepageScrapper import Bookshop4HomepageScrapper
from sheets_api.SheetsApi import SheetsApi


core_scheduler = BlockingScheduler()

logging.basicConfig()
logging.getLogger('apscheduler').setLevel(logging.DEBUG)


@core_scheduler.scheduled_job('cron', timezone='utc', hour=7, minute=00)
def main():
    scrapped_products = scrap_products()
    sheets_api = SheetsApi()
    sheets_api.modifier.append_data_to_output_worksheet(scrapped_products)


def scrap_products():
    active_scrappers = [
        Bookshop1HomepageScrapper(),
        Bookshop2HomepageScrapper(),
        Bookshop3HomepageScrapper(),
        Bookshop4HomepageScrapper()
    ]
    products = []
    for scrapper in active_scrappers:
        products += scrapper.get_books_data()
    return products


core_scheduler.start()
