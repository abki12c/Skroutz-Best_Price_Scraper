# Skroutz-Best_Price_Scraper

<img src="https://www.digitalpro.gr/wp-content/uploads/2020/09/Skroutz-BestPrice-%CE%A0%CF%8E%CF%82-%CE%B8%CE%B1-%CE%B5%CE%BD%CE%B9%CF%83%CF%87%CF%8D%CF%83%CE%BF%CF%85%CE%BD-%CF%84%CE%BF-eshop-%CF%83%CE%B1%CF%82-930x620.png" width="900" height="600">


A cli application that scrapes data from the two biggest price comparison websites in Greece : BestPrice and Skroutz. There's some shops on Best Price that don't exist on Skroutz, so this app provides a quick way to automate comparison between the two sites. 

The available functionalities are:

- Find the cheapest product on Skroutz
- Find the cheapest product on Best Price 
- Compare Skroutz and Best Price Prices
- Show reviews from Skroutz and Best Price
- Monitor the price of a certain product
- Save product info of all products in a specific category

The data are scaped using the json data sent to the website server and using Beautiful Soup for Best Price specifically

## Installation
Use the package manager pip to install the requirements
```
pip install -r requirements.txt
```

## Run
````
python main_program.py
````

## Config file

There's a config.ini file that is used for BestPrice scraping. The default settings are to use the Firefox browser with Selenium and the default path for the browser driver. You can change the driver path and browser type to chrome, edge or firefox. Firefox is the default browser because it didn't work on chrome on my system. 
