from bs4 import BeautifulSoup
import requests
import re


ticker = "9885.T"


class Information():
    results = ""
    shares_out = 0.0
    market_cap = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + \
            ticker + '/profile'
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_shares_out(self.find_data("Shares Out (MIL)"))
        self.set_market_cap(self.find_data("Market Cap (MIL)"))

    def clean_string(self, string):
        data = string.strip().replace(',', '')
        data = re.sub("[^0123456789.]", '', data)
        data = float(data)
        return data

    def find_data(self, keyword):
        data_pos = self.results.find(keyword)
        data_splice = self.results[data_pos:data_pos + 350].split(">")[4]
        data = self.clean_string(data_splice)
        return data

    def set_results(self, results):
        self.results = results

    def set_shares_out(self, value):
        self.shares_out = value

    def set_market_cap(self, value):
        self.market_cap = value

    def get_shares_out(self):
        return self.shares_out

    def get_market_cap(self):
        return self.market_cap


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
        return self.net_income


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
        return self.cash_and_eq

    def get_t_current_assets(self):
        return self.t_current_assets

    def get_t_liabilities(self):
        return self.t_liabilities


ticker_information = Information(ticker)
ticker_income_statement = IncomeStatement(ticker)
ticker_balance_sheet = BalanceSheet(ticker)

shares_out = ticker_information.get_shares_out()
market_cap = ticker_information.get_market_cap()

net_income = ticker_income_statement.get_net_income()

cash_and_eq = ticker_balance_sheet.get_cash_and_eq()
t_current_assets = ticker_balance_sheet.get_t_current_assets()
t_liabilities = ticker_balance_sheet.get_t_liabilities()

price = market_cap / shares_out

net_current_assets = t_current_assets - t_liabilities
net_cash = cash_and_eq - t_liabilities

price_to_earnings = market_cap / net_income
price_to_nca = market_cap / net_current_assets
price_to_net_cash = market_cap / net_cash
current_ratio = t_current_assets / t_liabilities
