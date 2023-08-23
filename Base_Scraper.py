from abc import ABC, abstractmethod
class Base_Scraper(ABC):
    def __init__(self):
        self.selected_products = []
        self.all_products = []

    @abstractmethod
    def categories_are_available(data):
        pass

    def select_items(self, products_number):
        "Selects the items from the same category, according to user input, stores them in a list and returns them"
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
        selected_products = [self.all_products[product_number - 1] for product_number in product_numbers_list]
        return selected_products

    @abstractmethod
    def process_items(self, pages, response):
        pass

    @abstractmethod
    def select_products(self):
        pass
    
    def lowest_price(self):
        "Finds the cheapest product and shows its information"
        self.select_products()
        self.selected_products.sort(key=lambda product: product["price"])
        cheapest_product = self.selected_products[0]
        print("Cheapest product details:" + "\n" +
              "- Name: " + cheapest_product["name"] + "\n" +
              "- Price: " + str(cheapest_product["price"]) + " €" + "\n" +
              "- Link: " + cheapest_product["link"])

        print("-----------------------------")