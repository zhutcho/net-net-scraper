from bs4 import BeautifulSoup
import requests
import re

TICKERS = [
    '2408.T',
    'OSN.OQ',
    '9885.T'
]


class BalanceSheet():

    results = ""

    cash_and_eq = 0.0
    t_current_assets = 0.0
    t_liabilities = 0.0

    def clean_string(self, string):
        data = string.strip().replace(',', '')
        data = re.sub("[^0123456789.]", '', data)
        data = float(data)
        return data

    def find_data(self, keyword):
        data_pos = self.results.find(keyword)
        data_splice = self.results[data_pos:data_pos + 250].split(">")[3]
        data = self.clean_string(data_splice)
        return data

    def set_results(self, results):
        self.results = results

    def set_cash_and_eq(self, value):
        self.cash_and_eq = value

    def set_t_current_assets(self, value):
        self.t_current_assets = value

    def set_t_liabilities(self, value):
        self.t_liabilities = value

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + \
            ticker + '/financials/balance-sheet-quarterly'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_cash_and_eq(self.find_data("Cash &amp; Equivalents"))
        self.set_t_current_assets(self.find_data("Total Current Assets"))
        self.set_t_liabilities(self.find_data("Total Liabilities"))

    def get_cash_and_eq(self):
        return self.cash_and_eq

    def get_t_current_assets(self):
        return self.t_current_assets

    def get_t_liabilities(self):
        return self.t_liabilities


charle_co = BalanceSheet("9885.T")

print(charle_co.get_cash_and_eq())
print(charle_co.get_t_current_assets())
print(charle_co.get_t_liabilities())
