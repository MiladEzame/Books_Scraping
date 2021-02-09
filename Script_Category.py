from bs4 import BeautifulSoup as bs
import csv
import requests
import Script
from urllib.parse import urlparse, urlunparse


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

# to be able to get the data from different books inside a page, get current url, parse it and get only domain name, add the "a href" tag to the link and make a request to access it
# once there, call all the methods from the previous script and scrape all data 
# get back to the category page by requesting it through the URL link above
# example : new_book_url = "https://books.toscrape.com/catalogue/" + "a href" link
# request that page then call the methods of Script.py on that page

def category_website_access(URL):
    req = requests.get(URL)
    soup = bs(req.content,"html.parser")
    soup.prettify("utf-8")
    return soup

def navigate_books_single_page(URL,soup):
    # parse urls and request them to access the data
    soup = category_website_access(URL)
    parsed = urlparse(URL)
    base_url = urlunparse(parsed)[:37]
    book_url = ""
    # using [::2] because couldn't find any specific tag for the links, there were 2 similar "a href" tags inside the ol class = row
    for books in soup.find("ol",{"class":"row"}).findAll("a")[::2]:
        books_src = books.get("href")
        book_url = books_src[9:]
        final_url = base_url + book_url
        req = requests.get(final_url)
        print(req)
        print(final_url)

def navigate_different_pages():
    # find the pagination and request the different pages 
    print("")

def scrape_data_from_product_page():
    # call all the functions from previous script
    print("")

def write_csv_all_books():
    # write all the books scraped from one category into a csv file
    print("")

if __name__ == "__main__":
    URL = "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"
    soup = category_website_access(URL)
    navigate_books_single_page(URL,soup)



"""
test = {"red" : 3, "blue" : 4, "black" : 5, "white" : 9}
with open ("test.csv","w",newline="") as file:
    writer = csv.writer(file)
    for key,value in test.items():
        writer.writerow([key,value])
    file.close()
"""