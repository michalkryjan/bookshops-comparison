import os

import gspread
from gspread import Worksheet, Client, Spreadsheet
from oauth2client.service_account import ServiceAccountCredentials
from pandas import DataFrame


class SheetsApi:
    def __init__(self):
        self.authorized_client = SheetsApiAuthenticator.authorize_client()
        self.selector = SheetsSelector(self.authorized_client)
        self.modifier = SheetsModifier(self.authorized_client, self.selector.output_worksheet)


class SheetsApiAuthenticator:
    SCOPES = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    @classmethod
    def authorize_client(cls) -> Client:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(cls.__get_service_account_creds_path(), cls.SCOPES)
        return gspread.authorize(credentials)

    @classmethod
    def __get_service_account_creds_path(cls):
        return os.path.join(cls.__get_current_dir_path(), 'keys', 'service_account_secret.json')

    @staticmethod
    def __get_current_dir_path():
        return os.path.dirname(os.path.abspath(__file__))


class SheetsSelector:
    def __init__(self, sheets_client: Client):
        self.client = sheets_client
        self.output_spreadsheet = self.__get_output_spreadsheet()
        self.output_worksheet = self.__get_output_worksheet()

    def __get_output_spreadsheet(self) -> Spreadsheet:
        return self.client.open_by_key(os.getenv('OUTPUT_SPREADSHEET_KEY'))

    def __get_output_worksheet(self) -> Worksheet:
        return self.output_spreadsheet.worksheet('data1')


class SheetsModifier:
    def __init__(self, sheets_client: Client, output_worksheet: Worksheet):
        self.client = sheets_client
        self.output_worksheet = output_worksheet

    def append_data_to_output_worksheet(self, data: dict):
        params = {'valueInputOption': 'USER_ENTERED'}
        body = {'values': DataFrame(data).values.tolist()}
        self.output_worksheet.spreadsheet.values_append(f'{self.output_worksheet.title}!A2:L2', params, body)

