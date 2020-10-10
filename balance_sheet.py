from lxml import html
from bs4 import BeautifulSoup
import requests

BASE_URL = [
    'https://www.reuters.com/companies/2408.T/financials/balance-sheet-quarterly',
    'https://www.reuters.com/companies/OSN.OQ/financials/balance-sheet-quarterly',
    'https://www.reuters.com/companies/9885.T/financials/balance-sheet-quarterly'
]


def clean_data(data):
    data = data.strip().replace(",", "")
    data = float(data)
    return data


for url in BASE_URL:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    results = soup.find(id='__next')

    cash_and_eq_position = results.prettify().find("Cash &amp; Equivalents") + 188
    cash_and_eq = clean_data(results.prettify(
    )[cash_and_eq_position: cash_and_eq_position + 11])
    print(cash_and_eq)

    total_ca_position = results.prettify().find("Total Current Assets") + 186
    total_ca = clean_data(results.prettify(
    )[total_ca_position: total_ca_position + 11])
    print(total_ca)

    total_liab_position = results.prettify().find("Total Liabilities") + 184
    total_liab = clean_data(results.prettify(
    )[total_liab_position: total_liab_position + 11])
    print(total_liab)
