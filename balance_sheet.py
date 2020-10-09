from lxml import html
from bs4 import BeautifulSoup
import requests

BASE_URL = [
    'https://www.reuters.com/companies/2408.T/financials/balance-sheet-quarterly',
    'https://www.reuters.com/companies/OSN.OQ/financials/balance-sheet-quarterly',
    'https://www.reuters.com/companies/9885.T/financials/balance-sheet-quarterly'
]

for url in BASE_URL:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    print(soup)
