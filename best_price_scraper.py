import time
import configparser
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC


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
    return len(driver.find_elements(By.CLASS_NAME,"pagination.pagination-has-next"))!=0


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
        categories_tag = driver.find_elements(By.CLASS_NAME, "categories__title")
        categories_tag = categories_tag[1:]
        categories = [category.text for category in categories_tag]
        
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

    time.sleep(2)

    if (pages_are_multiple()):
        unordered_list = driver.find_element(By.CLASS_NAME, "pagination.pagination-has-next")
        pages_number = int(unordered_list.find_elements(By.TAG_NAME, "a")[-2].text)
    else:
        pages_number = 1
