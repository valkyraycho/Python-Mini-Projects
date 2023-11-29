from bs4 import BeautifulSoup
import requests
from pprint import PrettyPrinter

printer = PrettyPrinter()

url = "https://coinmarketcap.com/"

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
result = requests.get(url, headers=headers)
page = BeautifulSoup(result.content, "html.parser")

tbody = page.find("tbody")
trs = tbody.contents # iterable tags
# we can access siblings, parent, children, descendants, etc
# print(list(trs[0].children)[0])

# scrape the website and store information

prices = {}

for tr in trs:
    name, price = tr.contents[2:4] # getting just the name and the price
    try:
        name_fixed = name.find("p").get_text() # or name.p.string
    except(AttributeError):
        name_fixed = name.find_all("span")[1].get_text()
    price_fixed = price.get_text()

    prices[name_fixed] = price_fixed


printer.pprint(prices)

