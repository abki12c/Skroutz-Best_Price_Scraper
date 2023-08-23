
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
    print("----------------------------------------------------------")
    print("1. Find the cheapest product on Skroutz")
    print("2. Find the cheapest product on Best Price")
    print("3. Compare Skroutz and Best Price Prices")
    print("4. Show reviews from Skroutz and Best Price")
    print("5. Monitor the price of a certain product")
    print("----------------------------------------------------------")
    # TODO: 2,3,4,5

    choice = input("Choose the desired functionality number: ")
    while(choice not in ['1','2','3','4','5']):
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

            answer = input("Do you want to select another product?(Y/N) ")
            answer.lower()
            while(answer not in ["yes","no","y","n"]):
                answer = input("Wrong answer, enter again: ")

        all_products.extend(skroutz.selected_products)

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
        print("Cheapest product details:" + "\n" +
              "- Name: " + cheapest_product["name"] + "\n" +
              "- Price: " + str(cheapest_product["price"]) + " €" + "\n" +
              "- Link: " + cheapest_product["link"])

        print("-----------------------------")

