from bs4 import BeautifulSoup as bs
import csv
import requests
import Script
from urllib.parse import urlparse, urlunparse


# information to gather :
"""
product_page_url ok
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

def category_website_access(URL):
    req = requests.get(URL)
    soup = bs(req.content,"html.parser")
    soup.prettify("utf-8")
    return soup

def navigate_books_single_page(URL,soup,header_list, value_list):
    # parse urls and request them to access the data
    soup = category_website_access(URL)
    parsed = urlparse(URL)
    base_url = urlunparse(parsed)[:37]
    book_url = ""
    list_url_books = []
    # using [::2] because couldn't find any specific tag for the links, there were 2 similar "a href" tags inside the ol class = row
    for books in soup.find("ol",{"class":"row"}).findAll("a")[::10]:
        books_src = books.get("href")
        book_url = books_src[9:]
        final_url = base_url + book_url
        list_url_books.append(final_url)
        req = requests.get(final_url)
    return list_url_books

def navigate_different_pages():
    # find the pagination and request the different pages 
    print("")

def scrape_data_from_product_page(list_url_books,soup,header_list, value_list,csv_name):
    # call all the functions from previous script
    Script.add_header_csv(header_list)
    for urls in list_url_books:
        soup = category_website_access(urls)
        value_list.append(Script.add_data_category(value_list,soup,urls))
        value_list.append(Script.add_data_img(value_list,soup,urls))
        value_list.append(Script.add_data_title(value_list,soup,urls))
        value_list.append(Script.add_data_product_page_url(value_list,soup,urls))
        value_list.append(Script.add_data_table_values(value_list,soup,urls))
        print(value_list)
        write_csv_all_books(header_list,value_list,csv_name)
    return value_list

def write_csv_all_books(header_list, value_list,csv_name):
    with open(csv_name, 'w',encoding='utf-8',newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        header_list = Script.add_header_csv(header_list)
        writer = csv.writer(file,delimiter=";")
        writer.writerow(header_list)
        writer.writerow(value_list)
    file.close()

if __name__ == "__main__":
    URL = "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"
    soup = category_website_access(URL)
    csv_name = "books_one_category_scraped.csv"
    csv_headers = []
    csv_values = []
    list_urls = navigate_books_single_page(URL,soup,csv_headers,csv_values)
    scrape_data_from_product_page(list_urls,soup,csv_headers,csv_values,csv_name)