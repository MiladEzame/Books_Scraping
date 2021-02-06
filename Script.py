from bs4 import BeautifulSoup as bs
import csv
import requests


# information to gather :
"""
product_page_url 
universal_ product_code (upc) 
title 
price_including_tax 
price_excluding_tax 
number_available 
product_description 
category 
review_rating 
image_url 
"""

# for multiple pages, change the number into a variable to increment 
# example with this url : https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-[number_to_increment].html

# url of the website to scrape
URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# attempt to access the url, if req = 200 -> (success) 
# instantiate a soup object with 2 parameters : the data content(can be text or other methods) needed and the type to parse  
req = requests.get(URL)
soup = bs(req.text, "html.parser")
print(req)
