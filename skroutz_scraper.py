import csv
import time
import os
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
        category = response_data['category']
        return len(category) == 0

    def process_items(self, pages, response):
        base_url = response.url
        current_page_number = 1
        for i in tqdm(range(1, pages + 1), desc="Processing page items...", colour="GREEN", unit="page"):
            current_url = f"{base_url}&page={current_page_number}"
            response = self.session.get(current_url, headers=self.headers)

            self.check_response_status(response)

            response_data = response.json()

            products_list = [product for product in response_data["skus"]]

            for product in products_list:
                product_name = product["name"]
                product_link = "https://www.skroutz.gr" + product["sku_url"]
                if(product["obsolete"]):
                    # Product is unavailable
                    continue
                else:
                    product_price = product["price"].replace('€', '').replace(".", "").replace(',', '.')
                    product_price = float(product_price)


                product_info = {
                    "name": product_name,
                    "link": product_link,
                    "price": product_price
                }
                self.all_products.append(product_info)

            current_page_number += 1



    def select_products(self):
        product = input("Enter the product you're looking for on Skroutz: ")
        product = super().convert_language(product)
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
        self.selected_products.extend(self.select_items(products_number))


    def save_products_to_csv(self):
        product = input("Enter the product you're looking for on Skroutz: ")
        product = super().convert_language(product)
        product.replace(" ", "+")

        self.params["keyphrase"] = product

        session = tls_client.Session(

            client_identifier="chrome112",

            random_tls_extension_order=True

        )

        response = session.get('https://www.skroutz.gr/search.json', params=self.params, headers=self.headers)
        response_data = response.json()

        if ("redirectUrl" in response_data):
            url = response_data["redirectUrl"].replace("html", "json")
            response = session.get(url, params=self.params, headers=self.headers)
            response_data = response.json()

        if (self.categories_are_available(response_data)):
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
            url = categories[category_number - 1]["link"].replace("html", "json")
            response = session.get(url, headers=self.headers, params=self.params)

            if (response.status_code == 301):
                new_url = response.headers['Location']
                print(new_url)
                response = requests.get(new_url, headers=self.headers)
            response_data = response.json()

        pages = response_data['page']['total_pages']

        self.process_items(pages, response)

        with open("data/info.csv","w",encoding="utf-8-sig", newline='') as csvfile:
            fieldnames = ["name","link","price"]
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            writer.writeheader()
            for product in self.all_products:
                product['name'] = product['name'].encode('utf-8', errors='replace').decode('utf-8', errors='replace')
                writer.writerow(product)

        print("file has been saved")

    def monitor_product(self, checking_frequency = 60):
        # if the csv file for monitoring products doesn't exist, create it
        if(not os.path.exists("monitored_products.csv")):
            with open("monitored_products.csv", "w", newline="") as csvfile:
                header = ["Name", "Price_Alert", "Current_Price", "Link"]
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(header)

        with open("monitored_products.csv","r+",newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            csvwriter = csv.writer(csvfile)

            products_available = True
            # Check if there's only one row (header) left in the file
            try:
                next(csvreader)
                next(csvreader)
                # If we reach here, there's at least one more row after the header
            except StopIteration:
                # If StopIteration is raised, there are no more rows
                products_available = False

            if (products_available is False):
                link = input("There's no available products in the csvfile. Enter the link here: ")
                idx = link.rindex("/")
                new_link = link[:idx+1] + "filter_products.json?"
                name = input("Enter the product name: ")
                response = self.session.get(new_link, headers=self.headers)
                response_data = response.json()
                current_price = response_data["price_min"].replace(",",".").replace("€","")
                current_price = float(current_price)
                price_alert = int(input(f"Enter the price point at which you want to receive a notification if the price is the same or lower. The current price is {current_price}: "))
                row_data = [name,price_alert,current_price,link]
                csvwriter.writerow(row_data)


            # show the available products to monitor
            products_row_numbers = []
            row_number = 1
            csvfile.seek(0)
            print() # empty line
            for row in csvreader:
                if len(row)>0 and row!=['Name', 'Price_Alert', 'Current_Price', 'Link']:
                    print("Row: " + str(row_number) + "-> Name: " + row[0] + ", Price_Alert: ", row[1] + ", Current_Price: " + row[2] + ", Link: " + row[3])
                    products_row_numbers.append(row_number)
                row_number+=1


            print()  # empty line
            print("-----------------------------")
            product_numbers_string = input("Enter the desired product to monitor based on the row number. To select more than one products seperate them with commas. If you want to monitor all the products simply type all: ")
            product_numbers_list = []
            commas = product_numbers_string.count(",")
            product_numbers_are_incorrect = True
            while (product_numbers_are_incorrect):
                if (commas == 0):
                    if (int(product_numbers_string) not in products_row_numbers):
                        product_numbers_string = input("Wrong number, enter again: ")
                        commas = product_numbers_string.count(",")
                    elif(product_numbers_string.lower() == "all"):
                        product_numbers_list.append(products_row_numbers)
                        product_numbers_are_incorrect = False
                    else:
                        product_numbers_list.append(int(product_numbers_string))
                        product_numbers_are_incorrect = False
                else:
                    product_numbers_string = product_numbers_string.split(",")
                    if (any(int(product_number) not in products_row_numbers for product_number in
                            product_numbers_string)):
                        product_numbers_string = input("One or more numbers are incorrect, enter again: ")
                        commas = product_numbers_string.count(",")
                    else:
                        product_numbers_list = [int(num) for num in product_numbers_string]
                        product_numbers_are_incorrect = False

            print()
            print("-----------------------------")
            # save the selected products
            selected_products = [self.all_products[product_number - 1] for product_number in product_numbers_list]

            while(product_number not in products_row_numbers):
                product_number = int(input("The provided row number is incorrect, enter again: "))

            csvfile.seek(0)

            for _ in range(product_number-1):
                next(csvreader)

            name, price_alert, current_price, link = next(csvreader)
            product = {
                "name": name,
                "price_alert": float(price_alert),
                "current_price": current_price,
                "link": link,
                "product_number": product_number
            }



            print("Price Monitoring has began", end="\n\n")
            while(True):
                idx = product["link"].rindex("/")
                new_link = link[:idx + 1] + "filter_products.json?"
                response = self.session.get(new_link, headers=self.headers)
                response_data = response.json()
                # check
                current_minimum_price = float(response_data["price_min"].replace('€', '').replace(',', '.'))
                if(current_minimum_price<product["price_alert"]):
                    print(f"There's a new minimum price for {product['name']} which is {current_minimum_price}€")
                    print(f"Link: {product['link']}")
                    csvfile.seek(0)
                    # save the new price in the csv file
                    for line_number, row in enumerate(csvreader, start=1):
                        if line_number == product["product_number"]:
                            # Modify the third column
                            row[2] = current_minimum_price
                            new_row = row
                            break
                    break
                print("Checked the current price. Price hasn't changed")
                time.sleep(checking_frequency)

        # open the file to read the existing data and change the new data with the new minimum price
        with open("monitored_products.csv", "r", newline="") as csvfile:
            csvreader = csv.reader(csvfile)
            existing_data = list(csvreader)
            existing_data[product["product_number"] - 1] = new_row

        # open the file to write the new minimum price
        with open("monitored_products.csv", "w", newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(existing_data)