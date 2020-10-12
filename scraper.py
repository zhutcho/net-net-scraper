from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import requests
import re
import csv
import itertools
import random
from time import sleep


gecko_install = GeckoDriverManager().install()
driver = webdriver.Firefox(executable_path=gecko_install)
driver2 = webdriver.Firefox(executable_path=gecko_install)
driver3 = webdriver.Firefox(executable_path=gecko_install)


def clean_string(string):
    data = string.strip().replace(',', '')
    data = re.sub("[^0123456789.()]", '', data)
    if data[0] == '(':
        data = re.sub("[^0123456789.]", '', data)
        data = '-' + data
    data = float(data)
    return data


def find_data(results, keyword, index):
    data_pos = results.find(keyword)
    data_replace = results[data_pos:data_pos + 1000].replace('<', '>')
    data_splice = data_replace.split('>')[index]
    data = clean_string(data_splice)
    return data


class Information():
    results = ""
    price = 0.0
    shares_out = 0.0
    market_cap = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + ticker
        driver.get(URL)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_price(find_data(self.results, "Latest Trade", 4))
        self.set_shares_out(find_data(self.results, "Shares Out (MIL)", 8))
        self.set_market_cap(find_data(self.results, "Market Cap (MIL)", 8))

    def set_results(self, results):
        self.results = results

    def get_price(self):
        return self.price

    def set_price(self, value):
        self.price = value

    def get_shares_out(self):
        return self.shares_out

    def set_shares_out(self, value):
        self.shares_out = value

    def get_market_cap(self):
        return self.market_cap

    def set_market_cap(self, value):
        self.market_cap = value


class IncomeStatement():
    results = ""
    net_income = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + \
            ticker + '/financials/income-statement-annual'
        driver2.get(URL)
        soup = BeautifulSoup(driver2.page_source, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_net_income(
            find_data(self.results, "Diluted Net Income", 6))

    def set_results(self, results):
        self.results = results

    def get_net_income(self):
        return self.net_income

    def set_net_income(self, value):
        self.net_income = value


class BalanceSheet():
    results = ""
    date = ""
    cash_and_eq = 0.0
    t_current_assets = 0.0
    t_liabilities = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + \
            ticker + '/financials/balance-sheet-quarterly'
        driver3.get(URL)
        soup = BeautifulSoup(driver3.page_source, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_cash_and_eq(
            find_data(self.results, "Cash and Short Term Investments", 6))
        self.set_t_current_assets(
            find_data(self.results, "Total Current Assets", 6))
        self.set_t_liabilities(find_data(self.results, "Total Liabilities", 6))

    def set_results(self, results):
        self.results = results

    def get_cash_and_eq(self):
        return self.cash_and_eq

    def set_cash_and_eq(self, value):
        self.cash_and_eq = value

    def get_t_current_assets(self):
        return self.t_current_assets

    def set_t_current_assets(self, value):
        self.t_current_assets = value

    def get_t_liabilities(self):
        return self.t_liabilities

    def set_t_liabilities(self, value):
        self.t_liabilities = value


def get_list():
    with open('tickers.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        data = list(itertools.chain.from_iterable(reader))[1:]
        csvfile.close()
    print(data)
    return data


def to_CSV():
    sleep_count = 0
    ticker_list = get_list()
    with open('net_net_data.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["ticker"] + ["pe"] + ["price to nca"] +
                        ["price to net cash"] + ["current ratio"])
        for ticker in ticker_list:
            print(ticker)
            ticker_information = Information(ticker)
            ticker_income_statement = IncomeStatement(ticker)
            ticker_balance_sheet = BalanceSheet(ticker)
            sleep(random.randint(2, 10))

            price = ticker_information.get_price()
            shares_out = ticker_information.get_shares_out()
            market_cap = ticker_information.get_market_cap()

            net_income = ticker_income_statement.get_net_income()

            cash_and_eq = ticker_balance_sheet.get_cash_and_eq()
            t_current_assets = ticker_balance_sheet.get_t_current_assets()
            t_liabilities = ticker_balance_sheet.get_t_liabilities()

            net_current_assets = t_current_assets - t_liabilities
            net_cash = cash_and_eq - t_liabilities

            price_to_earnings = round(market_cap / net_income, 2)
            price_to_nca = round(market_cap / net_current_assets, 2)
            price_to_net_cash = round(market_cap / net_cash, 2)
            current_ratio = round(t_current_assets / t_liabilities, 2)
            writer.writerow([ticker] + [price_to_earnings] +
                            [price_to_nca] + [price_to_net_cash] + [current_ratio])


to_CSV()
