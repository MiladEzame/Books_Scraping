from bs4 import BeautifulSoup as bs
import csv
import requests
import script
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

def category_website_access(url):
    req = requests.get(url)
    soup = bs(req.content,"html.parser")
    soup.prettify("utf-8")
    return soup

def navigate_books_single_page(url):
    # parse urls and request them to access the data
    parsed = urlparse(url)
    base_url = urlunparse(parsed)[:37]
    book_url = ""
    urls_books = []
    # using [::2] because couldn't find any specific tag for the links, there were 2 similar "a href" tags inside the ol class = row
    for books in soup.find("ol",{"class":"row"}).findAll("a")[::2]:
        books_src = books.get("href")
        book_url = books_src[9:]
        final_url = base_url + book_url
        urls_books.append(final_url)
        req = requests.get(final_url)
    return urls_books

def navigate_different_pages(url):
    parsed = urlparse(url)
    page = 1
    urls = []
    for page in range(1, 7):
        base_url = urlunparse(parsed)[:-10] + "page-{}.html".format(page)
        req = requests.get(base_url)
        urls.append(base_url)
    return urls
        

def scrape_data_from_product_page(urls_books, values,csv_name):
    # call all the functions from previous script
    for urls in urls_books:
        soup = category_website_access(urls)
        values.append(script.add_data_category(values,soup,urls))
        values.append(script.add_data_img(values,soup,urls))
        values.append(script.add_data_title(values,soup,urls))
        values.append(script.add_data_product_page_url(values,soup,urls))
        for value_text in soup.findAll("td"):
            values.append(value_text.get_text())
        write_csv_values(values,csv_name)
        values = []

def write_csv_headers(headers,csv_name):
    with open(csv_name, 'w',encoding='utf-8',newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        headers = script.add_header_csv(headers)
        writer = csv.writer(file,delimiter=";")
        writer.writerow(headers)
    file.close()

def write_csv_values(values,csv_name):
    with open(csv_name, 'a',encoding='utf-8',newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")
        writer.writerow(values)
    file.close()


if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html"
    soup = category_website_access(url)
    csv_name = "books_one_category_scraped.csv"
    csv_headers = []
    csv_values = []
    urls = navigate_books_single_page(url)
    write_csv_headers(csv_headers,csv_name)
    scrape_data_from_product_page(urls,csv_values,csv_name)
    #urls = navigate_different_pages(url)
    #crape_data_from_different_pages(urls,soup,csv_headers,csv_values,csv_name)