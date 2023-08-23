import requests
import tls_client
from tqdm import tqdm
from Base_Scraper import Base_Scraper


class skroutz_scraper(Base_Scraper):

    def __init__(self):
        super().__init__()
        self.headers = {
            'authority': 'www.skroutz.gr',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-US,en;q=0.9',
            'dnt': '1',
            'referer': 'https://www.skroutz.gr/search?keyphrase=witcher',
            'sec-ch-ua': '"Chromium";v="116", "Not)A;Brand";v="24", "Google Chrome";v="116"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
        }

        self.params = {
            'keyphrase': "",
            'page': '1',
        }

        self.session = tls_client.Session(

            client_identifier="chrome112",

            random_tls_extension_order=True

        )

    def categories_are_available(self, response_data):
        "Returns True if there are available categories to choose from and False if there aren't"
        category = response_data['category']
        return len(category) == 0

    def process_items(self, pages, response):
        "Processes all products from all the available pages and stores them in a list"
        base_url = response.url
        all_products = []
        current_page_number = 1
        for i in tqdm(range(1, pages + 1), desc="Processing page items...", colour="GREEN", unit="page"):
            current_url = f"{base_url}&page={current_page_number}"
            response = self.session.get(current_url, headers=self.headers)

            if(response.status_code!=200):
                exit("Page Unreachable")

            response_data = response.json()

            products_list = [product for product in response_data["skus"]]

            for product in products_list:
                product_name = product["name"]
                product_link = "https://www.skroutz.gr" + product["sku_url"]
                if(product["obsolete"]):
                    # Product is unavailable
                    continue
                else:
                    product_price = product["price"].replace('€', '').replace(',', '.')


                product_info = {
                    "name": product_name,
                    "link": product_link,
                    "price": product_price
                }
                self.all_products.append(product_info)

            current_page_number += 1

    def lowest_price(self):
        product = input("Enter the product you're looking for: ")
        product.replace(" ", "+")

        self.params["keyphrase"] = product

        session = tls_client.Session(

            client_identifier="chrome112",

            random_tls_extension_order=True

        )

        response = session.get('https://www.skroutz.gr/search.json', params=self.params, headers=self.headers)
        response_data = response.json()

        if("redirectUrl" in response_data):
            url = response_data["redirectUrl"].replace("html", "json")
            response = session.get(url, params=self.params, headers=self.headers)
            response_data = response.json()

        if(self.categories_are_available(response_data)) :
            print("categories are available")
            categories = [{"name": category["name"], "link": "https://www.skroutz.gr/" + category["url"]} for category in response_data["page"]["category_cards"]]

            print()  # empty tile
            print("Categories", end="\n\n")
            print("-----------------------------")
            i = 1
            for category in categories:
                print(str(i) + ". " + category["name"])
                i += 1

            print("-----------------------------", end="\n\n")
            category_number = input("Choose the category of the product: ")
            print()  # empty line
            while (int(category_number) not in [j for j in range(1, i + 1)]):
                category_number = input("Wrong number, enter again: ")

            category_number = int(category_number)

            # go to the right category
            url = categories[category_number-1]["link"].replace("html","json")
            response = session.get(url, headers=self.headers,params=self.params)

            if(response.status_code==301):
                new_url = response.headers['Location']
                print(new_url)
                response = requests.get(new_url,headers=self.headers)
            response_data = response.json()

        pages = response_data['page']['total_pages']

        self.process_items(pages, response)

        # print all products
        products_number = len(self.all_products)
        print("-----------------------------")
        for i in range(products_number):
            print(str(i + 1) + ": " + self.all_products[i]["name"])

        # Select product number(s) and save them in a list
        selected_products = self.select_items(products_number)
        # find the cheapest product
        selected_products.sort(key=lambda product: product["price"])
        cheapest_product = selected_products[0]
        print("Cheapest product details:" + "\n" +
              "- Name: " + cheapest_product["name"] + "\n" +
              "- Price: " + str(cheapest_product["price"]) + " €" + "\n" +
              "- Link: " + cheapest_product["link"])

        print("-----------------------------")