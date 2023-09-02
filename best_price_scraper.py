import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from Base_Scraper import Base_Scraper


class best_price_scraper(Base_Scraper):

    def __init__(self):
        super().__init__()
        self.headers = {
            'Accept': 'application/json',
            'Referer': 'https://www.bestprice.gr/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
            'X-Fromxhr': '1',
            'X-Theme': 'default',
            'X-Viewport': 'LG'
        }

    def categories_are_available(self, html_doc):
        "Returns True if there are available categories to choose from and False if there aren't"
        categories = html_doc.find_all(class_="categories__category")
        return len(categories) != 0

    def process_items(self, pages, response):
        base_url = response.url
        current_page_number = 1
        for i in tqdm(range(1, pages + 1), desc="Processing page items...", colour="GREEN", unit="page"):
            current_url = f"{base_url}&pg={current_page_number}"
            response = requests.get(current_url,headers=self.headers)

            if(response.status_code!=200):
                exit("Page Unreachable")

            data = response.json()
            html = data['html']

            html_doc = BeautifulSoup(html, 'html.parser')

            products_list = html_doc.find_all('div', {'data-id': True, 'data-cid': True})

            for product in products_list:
                product_name = product.find("h3").text.strip()
                product_link = "https://www.bestprice.gr" + product.find("h3").find("a")["href"]

                product_price = int(product['data-price']) / 100
                if(product_price==0):
                    # product unavailable
                    continue

                product_info = {
                    "name": product_name,
                    "link": product_link,
                    "price": product_price
                }
                self.all_products.append(product_info)

            current_page_number += 1

    def select_products(self):
        product = input("Enter the product you're looking for on Best Price: ")
        product.replace(" ","+")
        url = f"https://www.bestprice.gr/search?q={product}"

        response = requests.get(url, headers=self.headers)

        if (response.status_code != 200):
            exit("Page Unreachable")

        response_data = response.json()

        html = response_data["html"]

        html_doc = BeautifulSoup(html, 'html.parser')

        if(self.categories_are_available(html_doc)):
            categories_tag = html_doc.find_all(class_="categories__category")
            categories = [category["title"] for category in categories_tag]

            print()  # empty tile
            print("Categories", end="\n\n")
            print("-----------------------------")
            i = 1
            for category in categories:
                print(str(i) + ". " + category)
                i += 1

            print("-----------------------------", end="\n\n")
            category_number = input("Choose the category of the product: ")
            print()  # empty line
            while (int(category_number) not in [j for j in range(1, i + 1)]):
                category_number = input("Wrong number, enter again: ")

            category_number = int(category_number)

            # go to the right category
            link = "https://www.bestprice.gr" + html_doc.find("a", title=categories[category_number - 1], class_="categories__category")["href"]

            response = requests.get(link, headers=self.headers)
            response_data = response.json()

        js_data = json.loads(response_data["jsData"])
        if('totalPages' in js_data['PAGE']):
            # category has more than one product
            pages = js_data['PAGE']['totalPages']
            self.process_items(pages, response)
        else:
            # category has a single product
            product_info = {
                "name": js_data['PAGE']["product"]["title"],
                "link": "https://www.bestprice.gr/" + js_data['PAGE']["product"]["link"],
                "price": js_data['PAGE']["product"]["price"]//100
            }
            self.all_products.append(product_info)

        # print all products
        products_number = len(self.all_products)
        print("-----------------------------")
        for i in range(products_number):
            print(str(i + 1) + ": " + self.all_products[i]["name"])

        # Select product number(s) and save them in a list
        self.selected_products.extend(self.select_items(products_number))