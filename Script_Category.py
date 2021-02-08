from bs4 import BeautifulSoup as bs
import csv
import requests

# information to gather :
"""
product_page_url not ok
universal_ product_code (upc) ok 
title ok
price_including_tax ok
price_excluding_tax ok
number_available ok
product_description ok
category ok
review_rating ok
image_url ok
"""

# for multiple pages, change the number into a variable to increment 
# example with this url : https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-[number_to_increment].html


csv_headers = []
csv_values = []

# url of the website to scrape
URL = "https://books.toscrape.com/catalogue/category/books/nonfiction_13/page-"
# the page number that will be incremented inside a loop
page = 1

# attempt to access the url, if req = 200 -> (success) 
# instantiate a soup object with 2 parameters : the data content(can be text or other methods) needed and the type to parse  
req = requests.get(URL + str(page) + ".html")
soup = bs(req.text, "html.parser")
soup.prettify("utf-8")

# to be able to get the data from different books inside a page, get current url, parse it and get only domain name, add the "a href" tag to the link and make a request to access it
# once there call all the methods from the previous script and scrape all data 
# get back to the category page by requesting it through the URL link above
# example : new_book_url = "https://books.toscrape.com/catalogue/" + "a href link" 
# request that page then call the methods of Script.py on that page
# but HOW TO GET THE CURRENT URL ?


"""
test = {"red" : 3, "blue" : 4, "black" : 5, "white" : 9}
with open ("test.csv","w",newline="") as file:
    writer = csv.writer(file)
    for key,value in test.items():
        writer.writerow([key,value])
    file.close()
"""