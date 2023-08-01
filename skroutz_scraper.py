import configparser
import time
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException


def Setup():
    "Sets up the web driver with the customized configuration"
    global driver
    config = configparser.ConfigParser()
    config.read("config.ini")
    chrome_driver_path = config.get('General_settings', 'chrome_driver_path')
    chrome_options = Options()
    chrome_options.add_argument('--headless=new')
    if(chrome_driver_path =="0"):
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome(chrome_driver_path, options=chrome_options)

def no_categories_available():
    "Returns True if there are available categories to choose from and False if there aren't"
    return len(driver.find_elements(By.ID, "skus_result"))!=0

def pages_are_multiple():
    "returns True if the product category has multiple pages and False if not"
    return len(driver.find_elements(By.CLASS_NAME, "paginator")) != 0

def process_skroutz_items():
    global all_products
    base_url = driver.current_url
    all_products = []
    current_page_number = 1
    for i in tqdm(range(1, pages_number + 1), desc="Processing page items...", colour="GREEN", unit="page"):
        current_url = base_url + "&page=" + str(current_page_number)
        driver.get(current_url)

        WebDriverWait(driver, timeout=10).until(EC.url_to_be(current_url))
        WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.ID, "sku-list")))

        products_list = driver.find_elements(By.CLASS_NAME, "cf.card")

        for product in products_list:
            try:
                product_name = WebDriverWait(product, timeout=10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "a"))).get_attribute("title")
                product_link = WebDriverWait(product, timeout=10).until(
                    EC.presence_of_element_located((By.TAG_NAME, "a"))).get_attribute("href")
                try:
                    product_price_elem = WebDriverWait(product, timeout=6).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, "card-content"))).find_element(By.CLASS_NAME,
                                                                                                        "price").find_element(
                        By.TAG_NAME, "a")
                except NoSuchElementException:
                    continue
                product_price = float(
                    product_price_elem.text.strip().replace('από', '').replace('€', '').replace(',', '.'))
            except TimeoutException:
                continue

            product_info = {
                "name": product_name,
                "link": product_link,
                "page_number": current_page_number,
                "price": product_price
            }
            all_products.append(product_info)
        current_page_number += 1
    print("Processed all products")


def select_skroutz_items():
    print()  # empty line
    print("-----------------------------")
    product_numbers_string = input(
        "Select product(s) number(s) of the product(s) you want to choose. If products are more than one seperate them with commas: ")
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
    return  selected_products

def Scrape_Skroutz():
    global products_number, pages_number

    Setup()
    url = "https://www.skroutz.gr"
    driver.get(url)

    search = driver.find_element(By.ID,"search-bar-input")
    product = input("Enter the product you're looking for: ")
    search.send_keys(product)
    search.send_keys(Keys.RETURN)

    # returns true if there's options of categories to select from
    select_category = no_categories_available()


    # if there's categories to select, select one and browse to that category
    if(select_category):
        unordered_list = driver.find_element(By.CLASS_NAME, "scroll-area")
        categories_p  = unordered_list.find_elements(By.TAG_NAME, "p")
        categories = [category.text for category in categories_p]


        print() # empty tile
        print("Categories", end="\n\n")
        print("-----------------------------")
        i = 1
        for category in categories:
            print(str(i) + ". " + category)
            i+=1

        print("-----------------------------", end= "\n\n")
        category_number = input("Choose the category of the product: ")
        print()  # empty line
        while(int(category_number) not in [j for j in range(1,i+1)]):
            category_number = input("Wrong number, enter again: ")

        category_number = int(category_number)

        # go to the right category
        link = driver.find_element(By.LINK_TEXT,categories[category_number-1])
        link.click()

    time.sleep(2)


    if(pages_are_multiple()):
        unordered_list = driver.find_element(By.CLASS_NAME, "paginator")
        pages_number = int(unordered_list.find_elements(By.TAG_NAME, "a")[-2].text)
    else:
        pages_number = 1


    # save all the products from all the available pages to a list
    process_skroutz_items()


    # print all products
    products_number = len(all_products)
    print("-----------------------------")
    for i in range(products_number):
        print(str(i+1) + ": " + all_products[i]["name"])


    # Select product number(s) and save them in a list
    selected_products = select_skroutz_items()
    # find the cheapest product
    selected_products.sort(key=lambda product: product["price"])
    cheapest_product = selected_products[0]
    print("Cheapest product details:" + "\n" +
          "- Name: " + cheapest_product["name"] + "\n" +
          "- Price: " + str(cheapest_product["price"]) + " €" + "\n" +
          "- Link: " + cheapest_product["link"])

    print("-----------------------------")

    driver.quit()