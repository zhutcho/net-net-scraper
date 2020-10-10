from bs4 import BeautifulSoup
import requests
import re


ticker = "9885.T"


class IncomeStatement():
    results = ""
    net_income = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + \
            ticker + '/financials/income-statement-annual'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_net_income(self.find_data("Net Income After Taxes"))

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

    def set_net_income(self, value):
        self.net_income = value

    def get_net_income(self):
        return str(self.net_income)


class BalanceSheet():
    results = ""
    cash_and_eq = 0.0
    t_current_assets = 0.0
    t_liabilities = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + \
            ticker + '/financials/balance-sheet-quarterly'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_cash_and_eq(self.find_data("Cash &amp; Equivalents"))
        self.set_t_current_assets(self.find_data("Total Current Assets"))
        self.set_t_liabilities(self.find_data("Total Liabilities"))

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

    def get_cash_and_eq(self):
        return str(self.cash_and_eq)

    def get_t_current_assets(self):
        return str(self.t_current_assets)

    def get_t_liabilities(self):
        return str(self.t_liabilities)


ticker_income_statement = IncomeStatement(ticker)
ticker_balance_sheet = BalanceSheet(ticker)

print("Net Income: " + ticker_income_statement.get_net_income())

print("Cash & Equivalents: " + ticker_balance_sheet.get_cash_and_eq())
print("Total Current Assets: " + ticker_balance_sheet.get_t_current_assets())
print("Total Liabilities: " + ticker_balance_sheet.get_t_liabilities())
