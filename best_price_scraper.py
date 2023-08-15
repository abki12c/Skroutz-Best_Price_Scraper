import time
import configparser
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


def Setup():
    "Sets up the web driver with the customized configuration"
    global driver
    config = configparser.ConfigParser()
    config.read("config.ini")

    driver_path = config.get('General_settings', 'driver_path')
    browser_type = config.get("General_settings","browser_type").lower()

    browser_options = Options()

    if(browser_type == "chrome" ):
        browser_options.add_argument('--headless=new')
        if (driver_path == "0"):
            driver = webdriver.Chrome(options=browser_options)
        else:
            driver = webdriver.Chrome(driver_path, options=browser_options)
    elif(browser_type== "firefox"):
        browser_options.add_argument("-headless")
        if (driver_path == "0"):
            driver = webdriver.Firefox(options=browser_options)
        else:
            driver = webdriver.Firefox(driver_path, options=browser_options)
    elif(browser_type == "edge"):
        browser_options.add_argument("--headless=new")
        if (driver_path == "0"):
            driver = webdriver.Edge(options=browser_options)
        else:
            driver = webdriver.Edge(driver_path, options=browser_options)

def categories_are_available():
    "Returns True if there are available categories to choose from and False if there aren't"
    return len(driver.find_elements(By.CLASS_NAME, "categories__category"))!=0

def pages_are_multiple():
    "returns True if the product category has multiple pages and False if not"
    return len(driver.find_elements(By.CLASS_NAME,"pagination.pagination-has-next.pagination-has-hint"))!=0

def process_best_price_items(pages_number):
    "Processes all products from all the available pages and stores them in a list"
    global all_products
    base_url = driver.current_url
    all_products = []
    current_page_number = 1
    for i in tqdm(range(1, pages_number + 1), desc="Processing page items...", colour="GREEN", unit="page"):
        current_url = base_url + "&page=" + str(current_page_number)
        driver.get(current_url)

        WebDriverWait(driver, timeout=10).until(EC.url_to_be(current_url))
        WebDriverWait(driver, timeout=10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "p__products")))
        products_list = driver.find_element(By.CLASS_NAME, "p__products")


        window_height = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;")
        scroll_amount = window_height // 3  # Scroll one-third of the window height

        last_height = driver.execute_script("return document.body.scrollHeight")
        print("last height: " + str(last_height))
        while True:
            # Scroll down by the specified amount
            driver.execute_script(f"window.scrollTo(0, window.scrollY + {scroll_amount});")

            # Add a wait condition here to ensure new content is loaded
            try:
                WebDriverWait(driver, timeout=10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "p.p--portrait")))
            except TimeoutException:
                pass  # Handle the exception or continue scrolling

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            print("new height: " + str(new_height))
            if new_height == last_height:
                break
            last_height = new_height
        try:
            products_list = products_list.find_elements(By.CLASS_NAME, "p.p--portrait")
        except NoSuchElementException:
            products_list = products_list.find_elements(By.CLASS_NAME,"p")
        #products_list = products_list.find_elements(By.XPATH, ".//*")
        print(len(products_list))

        for product in products_list:
            try:
                product_name = WebDriverWait(product, timeout=10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "a")))[1].get_attribute("title")
                product_link = WebDriverWait(product, timeout=10).until(
                    EC.presence_of_all_elements_located((By.TAG_NAME, "a")))[1].get_attribute("href")
                try:
                    product_price_elem = WebDriverWait(product, timeout=6).until(EC.visibility_of_all_elements_located((By.TAG_NAME, "a")))[2].text
                except NoSuchElementException:
                    # Product is unavailable
                    continue
                product_price = product_price_elem.strip().replace('€', '').replace(',', '.')
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

        # Check if the pages are more than can be viewed in the website
        if(current_page_number==pages_number):
            unordered_list = driver.find_element(By.CLASS_NAME, "pagination.pagination-has-next")
            new_pages_number = int(unordered_list.find_elements(By.TAG_NAME, "a")[-2].text)
            if(new_pages_number>current_page_number):
                pages_number = new_pages_number

    print("Processed all products")

def select_best_price_items(products_number):
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
    Setup()
    url = "https://www.bestprice.gr/"
    driver.get(url)

    search = driver.find_element(By.CLASS_NAME,"search__field").find_element(By.NAME,"q")
    product = input("Enter the product you're looking for: ")
    search.send_keys(product)
    search.send_keys(Keys.RETURN)
    WebDriverWait(driver,10).until(EC.url_to_be("https://www.bestprice.gr/search?q="+product))

    # if there's categories to select, select one and browse to that category
    if(categories_are_available()):
        categories_tag = driver.find_elements(By.CLASS_NAME, "categories__category")
        categories = [category.get_attribute("title") for category in categories_tag]
        
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
        link = driver.find_element(By.LINK_TEXT, categories[category_number - 1]).get_attribute("href")
        driver.get(link)

    WebDriverWait(driver,10).until(EC.url_to_be(link))
    if (pages_are_multiple()):
        unordered_list = driver.find_element(By.CLASS_NAME, "pagination.pagination-has-next")
        pages_number = int(unordered_list.find_elements(By.TAG_NAME, "a")[-2].text)
    else:
        pages_number = 1
    # save all the products from all the available pages to a list
    process_best_price_items(pages_number)

    # print all products
    products_number = len(all_products)
    print("-----------------------------")
    for i in range(products_number):
        print(str(i + 1) + ": " + all_products[i]["name"])

    # Select product number(s) and save them in a list
    selected_products = select_best_price_items(products_number)
    # find the cheapest product
    selected_products.sort(key=lambda product: product["price"])
    cheapest_product = selected_products[0]
    print("Cheapest product details:" + "\n" +
          "- Name: " + cheapest_product["name"] + "\n" +
          "- Price: " + str(cheapest_product["price"]) + " €" + "\n" +
          "- Link: " + cheapest_product["link"])

    print("-----------------------------")

    driver.quit()