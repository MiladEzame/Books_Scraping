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

def navigate_books_single_page(soup, url):
    parsed = urlparse(url)
    end_url = parsed.path.split("/")
    mid_url = ""
    for path in end_url[1:2]:
        mid_url = mid_url + path + "/"
    base_url = parsed.scheme + "://" + parsed.netloc + "/" + mid_url
    book_url = ""
    urls_books = []
    # using [::2] because couldn't find any specific tag for the links, there were 2 similar "a href" tags inside the ol class = row
    for books in soup.find("ol",{"class":"row"}).findAll("a")[::2]:
        books_src = books.get("href")
        book_url = books_src[9:]
        final_url = base_url + book_url
        print(final_url)
        urls_books.append(final_url)
    return urls_books

def scrap_all_books_one_category(soup, url, values, csv_name):
    if soup.find("li",{"class":"current"}):
        next_page = soup.find("li",{"class":"current"}).text.strip()
        next_page = next_page.split(" ")
        max_page = int(next_page[-1])
    else: 
        max_page = 1
    parsed = urlparse(url)
    end_url = parsed.path.split("/")
    mid_url = ""
    for path in end_url[1:5]:
        mid_url = mid_url + path + "/"
    base_url = parsed.scheme + "://" + parsed.netloc + "/" + mid_url
    for page in range(1, max_page+1):
        next_url = base_url + "page-{}.html".format(page)   
        urls = [] 
        req = requests.get(next_url)    
        soup = bs(req.content,"html.parser")
        if req.status_code == 200:
            urls = (navigate_books_single_page(soup, next_url))
            scrape_data_from_product_page(urls, values, csv_name)
            write_csv_nextline(csv_name)
        else:
            next_url = base_url + "index.html" 
            req = requests.get(next_url) 
            soup = bs(req.content,"html.parser")
            urls = (navigate_books_single_page(soup, next_url))
            scrape_data_from_product_page(urls, values, csv_name)
            break

def scrape_data_from_product_page(urls_books, values, csv_name):
    # call all the functions from previous script
    for urls in urls_books:
        soup = category_website_access(urls)
        values.append(script.add_data_category(values, soup,urls))
        values.append(script.add_data_img(values, soup, urls))
        values.append(script.add_data_title(values, soup, urls))
        values.append(script.add_data_product_page_url(values, soup, urls))
        for value_text in soup.findAll("td"):
            values.append(value_text.get_text())
        write_csv_values(values,csv_name)
        values = []

def write_csv_headers(headers, csv_name):
    with open(csv_name, 'w', encoding='utf-8', newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        headers = script.add_header_csv(headers)
        writer = csv.writer(file,delimiter=";")
        writer.writerow(headers)
    file.close()

def write_csv_nextline(csv_name):
    with open(csv_name, 'a', encoding='utf-8', newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")
        writer.writerow(" ")
        file.close()

def write_csv_values(values, csv_name):
    with open(csv_name, 'a', encoding='utf-8', newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")
        writer.writerow(values)
        file.close()


if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/category/books/childrens_11/index.html"
    # argparse 
    soup = category_website_access(url)
    csv_name = "books_one_category_scraped.csv"
    csv_headers = []
    csv_values = []
    write_csv_headers(csv_headers,csv_name)
    scrap_all_books_one_category(soup, url, csv_values, csv_name)
