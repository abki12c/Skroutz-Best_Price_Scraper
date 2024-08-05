import configparser
import time
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException, InvalidArgumentException
from selenium.webdriver import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
from Base_Scraper import Base_Scraper
import json


class best_price_scraper(Base_Scraper):

    def __init__(self):
        super().__init__()
        self.setup()


    def setup(self):
        "Sets up the web driver with the customized configuration"
        global driver
        config = configparser.ConfigParser()
        config.read("config.ini")

        driver_path = config.get('General_settings', 'driver_path')
        browser_type = config.get("General_settings", "browser_type").lower()

        if (browser_type == "chrome"):
            browser_options = webdriver.ChromeOptions()
            browser_options.add_argument('--headless=new')
            if (driver_path == "0"):
                driver = webdriver.Chrome(options=browser_options)
            else:
                driver = webdriver.Chrome(driver_path, options=browser_options)
        elif (browser_type == "firefox"):
            browser_options = webdriver.FirefoxOptions()
            browser_options.add_argument("-headless")
            if (driver_path == "0"):
                driver = webdriver.Firefox(options=browser_options)
            else:
                driver = webdriver.Firefox(driver_path, options=browser_options)
        elif (browser_type == "edge"):
            browser_options = webdriver.EdgeOptions()
            browser_options.add_argument("--headless=new")
            if (driver_path == "0"):
                driver = webdriver.Edge(options=browser_options)
            else:
                driver = webdriver.Edge(driver_path, options=browser_options)


    def categories_are_available(self):
        "Returns True if there are available categories to choose from and False if there aren't"
        return len(driver.find_elements(By.CLASS_NAME, "categories__category")) != 0

    def process_items(self, products_number):
        "Processes all products from all the available pages and stores them in a list"

        processed_product_links = set()
        with tqdm(total=products_number, desc="Processing product items...", colour="GREEN", unit="product") as pbar:

            while len(self.all_products) < products_number:

                products_list = WebDriverWait(driver, timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME, "p__products")))

                window_height = driver.execute_script("return window.innerHeight || document.documentElement.clientHeight || document.body.clientHeight;")
                last_height = driver.execute_script("return document.body.scrollHeight")
                scroll_pause_time = 2  # Adjust this based on how fast new content loads

                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(scroll_pause_time)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                try:
                    products_info_list = products_list.find_elements(By.XPATH, "./child::*")
                    products_info_list = [element for element in products_info_list if 'p__products-section' not in element.get_attribute('class')]
                except NoSuchElementException:
                    print("No such element")
                    products_info_list = products_list.find_elements(By.CLASS_NAME, "p")

                products_number = len(products_info_list)

                i = 0
                for product in products_info_list:
                    try:
                        product_element = product.find_element(By.CLASS_NAME, "p__meta")
                        product_name = WebDriverWait(product_element, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, "a"))).get_attribute("title")
                        product_link = WebDriverWait(product_element, timeout=10).until(EC.presence_of_element_located((By.TAG_NAME, "a"))).get_attribute("href")

                        review_score = reviews_count = 0
                        script = driver.find_elements(By.XPATH, '//script[@type="application/ld+json"]')[-1].get_attribute("innerHTML")
                        products = json.loads(script)
                        products = products["itemListElement"]
                        if "aggregateRating" in products[i]["item"]:
                            review_score = products[i]["item"]["aggregateRating"]["ratingValue"]
                            reviews_count = products[i]["item"]["aggregateRating"]["reviewCount"]



                        if product_link in processed_product_links:
                            continue  # Skip already processed products

                        try:
                            product_price_elem = product.find_element(By.CLASS_NAME, "p__price--current").text
                        except NoSuchElementException:
                            continue  # Product is unavailable

                        product_price = product_price_elem.strip().replace('€', '').replace('.', '').replace(",",".")
                    except TimeoutException:
                        continue

                    product_info = {
                        "name": product_name,
                        "link": product_link,
                        "price": float(product_price),
                        "review_score": review_score,
                        "reviews_count": reviews_count
                    }

                    self.all_products.append(product_info)
                    processed_product_links.add(product_link)

                    # Update tqdm progress bar
                    pbar.update(1)

                    if len(self.all_products) >= products_number:
                        break

                    i+=1

            print("Processed all products")

    def select_products(self):
        url = "https://www.bestprice.gr/"
        driver.get(url)

        WebDriverWait(driver, 10).until(EC.url_to_be(url))

        search = driver.find_element(By.CLASS_NAME, "search__field").find_element(By.NAME, "q")
        product = input("Enter the product you're looking for on BestPrice: ")
        search.send_keys(product)
        search.send_keys(Keys.RETURN)
        driver.get("https://www.bestprice.gr/search?q=" + product)
        time.sleep(2)

        # if there's categories to select, select one and browse to that category
        if (self.categories_are_available()):
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

            category_div = categories_tag[category_number-1].find_element(By.CLASS_NAME,"categories__cnt")
            products_number = int(category_div.text.replace("προϊόντα",""))

            # go to the right category
            link = categories_tag[category_number - 1].get_attribute("href")
            driver.get(link)



        # save all the products to a list
        self.process_items(products_number)

        # print all products
        products_number = len(self.all_products)
        print("-----------------------------")
        for i in range(products_number):
            print(str(i + 1) + ": " + self.all_products[i]["name"])

        # Select product number(s) and save them in a list
        self.selected_products = self.select_items(products_number)

        driver.quit()