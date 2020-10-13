from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import re
import csv
import itertools
import random
from time import sleep


gecko_install = GeckoDriverManager().install()
driver = webdriver.Firefox(executable_path=gecko_install)
driver_2 = webdriver.Firefox(executable_path=gecko_install)


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
    if keyword != "Price To Earnings (TTM)" and keyword != "Dividend (Yield %)":
        data = clean_string(data_splice)
    else:
        data = data_splice.strip()
    return data


class Information():
    results = ""
    price = 0.0
    pe_ttm = 0.0
    div_yield = 0.0
    shares_out = 0.0
    market_cap = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + ticker
        driver.get(URL)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        self.set_results(soup.find(id='__next').prettify())

        self.set_price(find_data(self.results, "Latest Trade", 4))
        self.set_pe_ttm(find_data(self.results, "Price To Earnings (TTM)", 8))
        self.set_div_yield(find_data(self.results, "Dividend (Yield %)", 8))
        self.set_shares_out(find_data(self.results, "Shares Out (MIL)", 8))
        self.set_market_cap(find_data(self.results, "Market Cap (MIL)", 8))

    def set_results(self, results):
        self.results = results

    def get_price(self):
        return self.price

    def set_price(self, value):
        self.price = value

    def get_pe_ttm(self):
        return self.pe_ttm

    def set_pe_ttm(self, value):
        self.pe_ttm = value

    def get_div_yield(self):
        return self.div_yield

    def set_div_yield(self, value):
        self.div_yield = value

    def get_shares_out(self):
        return self.shares_out

    def set_shares_out(self, value):
        self.shares_out = value

    def get_market_cap(self):
        return self.market_cap

    def set_market_cap(self, value):
        self.market_cap = value


class BalanceSheet():
    results = ""
    date = ""
    cash_and_eq = 0.0
    t_current_assets = 0.0
    t_liabilities = 0.0

    def __init__(self, ticker):
        URL = 'https://www.reuters.com/companies/' + \
            ticker + '/financials/balance-sheet-quarterly'
        driver_2.get(URL)
        soup = BeautifulSoup(driver_2.page_source, 'html.parser')
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
    return data


def to_CSV():
    sleep_count = 0
    ticker_list = get_list()
    with open('net_net_data_3.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["ticker"] + ["pe (ttm)"] + ["price to nca"] +
                        ["price to net cash"] + ["current ratio"] + ["dividend yield %"])
        for ticker in ticker_list:
            sleep_count += 1
            print(str(sleep_count) + '. ' + ticker)
            ticker_information = Information(ticker)
            sleep(random.random() * 5 + 10)
            ticker_balance_sheet = BalanceSheet(ticker)
            sleep(random.random() * 5 + 10)

            price = ticker_information.get_price()
            div_yield = ticker_information.get_div_yield()
            shares_out = ticker_information.get_shares_out()
            market_cap = ticker_information.get_market_cap()

            cash_and_eq = ticker_balance_sheet.get_cash_and_eq()
            t_current_assets = ticker_balance_sheet.get_t_current_assets()
            t_liabilities = ticker_balance_sheet.get_t_liabilities()

            net_current_assets = t_current_assets - t_liabilities
            net_cash = cash_and_eq - t_liabilities

            pe_ttm = ticker_information.get_pe_ttm()
            price_to_nca = round(market_cap / net_current_assets, 2)
            price_to_net_cash = round(market_cap / net_cash, 2)
            current_ratio = round(t_current_assets / t_liabilities, 2)
            writer.writerow([ticker] + [pe_ttm] + [price_to_nca] +
                            [price_to_net_cash] + [current_ratio] + [div_yield])

            if sleep_count % 6 == 0:
                sleep(random.random() * 120 + 150)
    driver.close()


to_CSV()
