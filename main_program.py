import sys
from skroutz_scraper import skroutz_scraper
from best_price_scraper import best_price_scraper
from colorama import Fore
from colorama import init as colorama_init


if(__name__=="__main__"):
    colorama_init(autoreset=True)

    print(Fore.GREEN + """
    
     ::::::::  :::    ::: :::::::::   ::::::::  :::    ::: ::::::::::: :::::::::                         :::::::::  :::::::::: :::::::: :::::::::::           :::::::::  :::::::::  ::::::::::: ::::::::  ::::::::::       ::::::::   ::::::::  :::::::::      :::     :::::::::  :::::::::: :::::::::  
    :+:    :+: :+:   :+:  :+:    :+: :+:    :+: :+:    :+:     :+:          :+:                          :+:    :+: :+:       :+:    :+:    :+:               :+:    :+: :+:    :+:     :+:    :+:    :+: :+:             :+:    :+: :+:    :+: :+:    :+:   :+: :+:   :+:    :+: :+:        :+:    :+: 
    +:+        +:+  +:+   +:+    +:+ +:+    +:+ +:+    +:+     +:+         +:+                           +:+    +:+ +:+       +:+           +:+               +:+    +:+ +:+    +:+     +:+    +:+        +:+             +:+        +:+        +:+    +:+  +:+   +:+  +:+    +:+ +:+        +:+    +:+ 
    +#++:++#++ +#++:++    +#++:++#:  +#+    +:+ +#+    +:+     +#+        +#+         +#++:++#++:++      +#++:++#+  +#++:++#  +#++:++#++    +#+               +#++:++#+  +#++:++#:      +#+    +#+        +#++:++#        +#++:++#++ +#+        +#++:++#:  +#++:++#++: +#++:++#+  +#++:++#   +#++:++#:  
           +#+ +#+  +#+   +#+    +#+ +#+    +#+ +#+    +#+     +#+       +#+                             +#+    +#+ +#+              +#+    +#+               +#+        +#+    +#+     +#+    +#+        +#+                    +#+ +#+        +#+    +#+ +#+     +#+ +#+        +#+        +#+    +#+ 
    #+#    #+# #+#   #+#  #+#    #+# #+#    #+# #+#    #+#     #+#      #+#                              #+#    #+# #+#       #+#    #+#    #+#               #+#        #+#    #+#     #+#    #+#    #+# #+#             #+#    #+# #+#    #+# #+#    #+# #+#     #+# #+#        #+#        #+#    #+# 
     ########  ###    ### ###    ###  ########   ########      ###     #########                         #########  ########## ########     ###    ########## ###        ###    ### ########### ########  ##########       ########   ########  ###    ### ###     ### ###        ########## ###    ### 
    
                            
    
    """)


    print("Welcome to this Webscraping program. Here are the functionalities of the program")

    while True:
        print("----------------------------------------------------------")
        print("1. Find the cheapest product on Skroutz")
        print("2. Find the cheapest product on Best Price")
        print("3. Compare Skroutz and Best Price Prices")
        print("4. Show reviews from Skroutz and Best Price")
        print("5. Monitor the price of a certain product")
        print("6. Save product info of all products in a specific category")
        print("7. Exit")
        print("----------------------------------------------------------")

        choice = input("Choose the desired functionality number: ")
        while(choice not in ['1','2','3','4','5','6','7']):
            choice = input("Wrong input. Please enter the desired functionality number: ")

        print() # empty line
        if(choice=='1'):
            skroutz = skroutz_scraper()
            skroutz.lowest_price()
        elif(choice=='2'):
            best_price = best_price_scraper()
            best_price.lowest_price()
        elif(choice=='3'):
            all_products = []
            # Select skroutz products
            skroutz = skroutz_scraper()
            answer = ' '
            while(answer not in ['no','n']):
                skroutz.select_products()

                answer = input("Do you want to select another product? (Y/N) ")
                answer.lower()
                while(answer not in ["yes","no","y","n"]):
                    answer = input("Wrong answer, enter again: ")

            all_products.extend(skroutz.selected_products)
            print() # empty line

            # Select best price products
            best_price = best_price_scraper()
            answer = ' '
            while (answer not in ['no', 'n']):
                best_price.select_products()

                answer = input("Do you want to select another product?(Y/N) ")
                answer.lower()
                while (answer not in ["yes", "no", "y", "n"]):
                    answer = input("Wrong answer, enter again: ")

            all_products.extend(best_price.selected_products)

            all_products.sort(key=lambda product: product["price"])
            cheapest_product = all_products[0]
            review_score = "Not Available"
            if(cheapest_product["review_score"]!=0):
                review_score = str(cheapest_product["review_score"])
            print("Cheapest product details:" + "\n" +
                "- Name: " + cheapest_product["name"] + "\n" +
                "- Price: " + str(cheapest_product["price"]) + " €" + "\n" +
                "- Review score: " + review_score + '\n' +
                "- Link: " + cheapest_product["link"])

            print("-----------------------------")

        elif(choice=='4'):
            all_products = []
            skroutz = skroutz_scraper()
            best_price = best_price_scraper()

            skroutz.select_products()
            best_price.select_products()

            all_products.extend(skroutz.selected_products)
            all_products.extend(best_price.selected_products)

            total_review_count = total_weighted_score = 0
            for product in all_products:
                total_review_count += product["reviews_count"]
                total_weighted_score += product["review_score"] * product["reviews_count"]

            weighted_average_review_score = 0
            if total_review_count!=0:
                weighted_average_review_score = total_weighted_score / total_review_count


            print("Revie Score: " + str(round(weighted_average_review_score,2)) if weighted_average_review_score !=0 else "Not Available")
            print("Reviews Count: " + str(total_review_count))

            print("-----------------------------")

        elif(choice=='5'):
            minutes = int(input("How frequently do you want to check for a price change in minutes? "))
            seconds = minutes*60
            skroutz = skroutz_scraper()
            skroutz.monitor_product(checking_frequency=seconds)

        elif(choice=='6'):
            skroutz = skroutz_scraper()
            skroutz.save_products_to_csv()
        else:
            sys.exit()