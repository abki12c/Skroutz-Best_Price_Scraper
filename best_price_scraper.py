import json
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm


def categories_are_available(html_doc):
    "Returns True if there are available categories to choose from and False if there aren't"
    categories = html_doc.find_all(class_="categories__category")
    return len(categories) != 0

def process_best_price_items(pages,response):
    "Processes all products from all the available pages and stores them in a list"
    global all_products
    base_url = response.url
    all_products = []
    current_page_number = 1
    for i in tqdm(range(1, pages + 1), desc="Processing page items...", colour="GREEN", unit="page"):
        current_url = f"{base_url}&pg={current_page_number}"
        response = requests.get(current_url,headers=headers)

        if(response.status_code!=200):
            exit("Page Unreachable")

        data = response.json()
        html = data['html']
        js_data = json.loads(data['jsData'])

        html_doc = BeautifulSoup(html, 'html.parser')

        products_list = html_doc.find_all('div', {'data-id': True, 'data-cid': True})

        for product in products_list:
            product_name = product.find_all("a")[1]["title"]
            product_link = "https://www.bestprice.gr" + product.find_all("a")[1]["href"]
            try:
                product_price_elem = product.find_all("a")[2].text
            except IndexError:
                # Product is unavailable
                continue
            product_price = product_price_elem.strip().replace('€', '').replace(',', '.')


            product_info = {
                "name": product_name,
                "link": product_link,
                "page_number": current_page_number,
                "price": product_price
            }
            all_products.append(product_info)

        current_page_number += 1


def select_items(products_number):
    "Selects the Best Price items according to user input, stores them in a list and returns them"
    print()  # empty line
    print("-----------------------------")
    product_numbers_string = input("Select product(s) number(s) of the product(s) you want to choose. If products are more than one seperate them with commas: ")
    product_numbers_list = []
    commas = product_numbers_string.count(",")
    product_numbers_are_incorrect = True
    while (product_numbers_are_incorrect):
        if (commas == 0):
            if (int(product_numbers_string) not in range(1, products_number + 1)):
                product_numbers_string = input("Wrong number, enter again: ")
                commas = product_numbers_string.count(",")
            else:
                product_numbers_list.append(int(product_numbers_string))
                product_numbers_are_incorrect = False
        else:
            product_numbers_string = product_numbers_string.split(",")
            if (any(int(product_number) not in range(1, products_number + 1) for product_number in
                    product_numbers_string)):
                product_numbers_string = input("One or more numbers are incorrect, enter again: ")
                commas = product_numbers_string.count(",")
            else:
                product_numbers_list = [int(num) for num in product_numbers_string]
                product_numbers_are_incorrect = False

    print()
    print("-----------------------------")
    # save the selected products
    selected_products = [all_products[product_number - 1] for product_number in product_numbers_list]
    return selected_products

def Scrape_Best_Price():
    global headers
    headers = {
        'Accept': 'application/json',
        'Referer': 'https://www.bestprice.gr/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
        'X-Fromxhr': '1',
        'X-Theme': 'default',
        'X-Viewport': 'LG'
    }

    product = input("Enter the product you're looking for: ")
    product.replace(" ","+")
    url = f"https://www.bestprice.gr/search?q={product}"

    response = requests.get(url, headers=headers)

    if (response.status_code != 200):
        exit("Page Unreachable")

    response_data = response.json()

    html = response_data["html"]

    html_doc = BeautifulSoup(html, 'html.parser')

    if(categories_are_available(html_doc)):
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

        response = requests.get(link, headers=headers)
        response_data = response.json()


    js_data = json.loads(response_data["jsData"])
    pages = js_data['PAGE']['totalPages']
    process_best_price_items(pages,response)

    # print all products
    products_number = len(all_products)
    print("-----------------------------")
    for i in range(products_number):
        print(str(i + 1) + ": " + all_products[i]["name"])

    # Select product number(s) and save them in a list
    selected_products = select_items(products_number)
    # find the cheapest product
    selected_products.sort(key=lambda product: product["price"])
    cheapest_product = selected_products[0]
    print("Cheapest product details:" + "\n" +
          "- Name: " + cheapest_product["name"] + "\n" +
          "- Price: " + str(cheapest_product["price"]) + " €" + "\n" +
          "- Link: " + cheapest_product["link"])

    print("-----------------------------")