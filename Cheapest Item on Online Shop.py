# web scraping with BeautifulSoup to find the cheapest item on an online shop

from bs4 import BeautifulSoup
import requests
import re

search_term = input("What product do you want to search for? ")

url = f"https://www.newegg.ca/p/pl?N=4131&d={search_term}&RN=4841"
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
result = requests.get(url, headers=headers)
page = BeautifulSoup(result.content, "html.parser")

# find the total number of pages
pages = int(page.find(class_="list-tool-pagination-text").find("strong").get_text().split("/")[1])

# to store the results
items_found = {}

# iterate through every page
for page in range(1, pages+1):
    url = f"https://www.newegg.ca/p/pl?N=4131&d={search_term}&RN=4841&page={page}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    result = requests.get(url, headers=headers)
    page = BeautifulSoup(result.content, "html.parser")

    # find the tag that includes the name of the item
    div = page.find(class_="item-cells-wrap border-cells items-grid-view four-cells expulsion-one-cell")
    
    # search for the names of the items with regex
    items = div.find_all(string=re.compile(search_term))
    
    # iterate through the items to find the prices and links
    for item in items:
        # find links first -> the parent tag is "a"
        if item.parent.name != "a":
            continue
        link = item.parent['href']

        # then find the parent that contains the price and locate the price text
        price_tag = item.find_parent(class_="item-container").find(class_="price-current").find_all(["strong","sup"])
        price = float(price_tag[0].get_text().replace(',','') + price_tag[1].get_text())
        
        items_found[item] = {"price": price, "link": link}

sorted_items = sorted(items_found.items(), key=lambda x: x[1]['price'])
items_found_sorted = {item[0]: item[1] for item in sorted_items}
print(items_found_sorted)