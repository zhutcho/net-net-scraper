from lxml import html
from bs4 import BeautifulSoup
import requests
import re

BASE_URL = [
    'https://www.reuters.com/companies/2408.T/financials/balance-sheet-quarterly',
    'https://www.reuters.com/companies/OSN.OQ/financials/balance-sheet-quarterly',
    'https://www.reuters.com/companies/9885.T/financials/balance-sheet-quarterly'
]


def clean_data(data):
    data = data.strip().replace(',', '')
    data = re.sub("[^0123456789.]", '', data)
    data = float(data)
    return data


def find_data(keyword):
    data_pos = results.find(keyword)
    data_splice = results[data_pos:data_pos + 250].split(">")[3]
    data = clean_data(data_splice)
    return data


for url in BASE_URL:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='__next').prettify()

    cash_and_equivalents = find_data("Cash &amp; Equivalents")
    total_current_assets = find_data("Total Current Assets")
    total_liabilities = find_data("Total Liabilities")

    print("Cash & Equivalents: " + str(cash_and_equivalents))
    print("Total Current Assets: " + str(total_current_assets))
    print("Total Liabilities: " + str(total_liabilities))
