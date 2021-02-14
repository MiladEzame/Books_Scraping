from bs4 import BeautifulSoup as bs
import csv
import requests
from urllib.request import urlopen
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

# for multiple pages, change the number into a variable to increment 
# example with this url : https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-[number_to_increment].html


def website_access(url):
    # url of the website to scrape
    # attempt to access the url, if req = 200 -> (success) 
    # instantiate a soup object with 2 parameters : the data content(can be text or other methods) needed and the type to parse  
    req = requests.get(url)
    soup = bs(req.text, "html.parser")
    soup.prettify("utf-8")
    return soup

def add_data_product_page_url(product_urls, soup,url):
    # get current url
    req = urlopen(url)
    return req.geturl()

def add_header_csv(headers):
    # add_header method : header lists for csv file
    headers = ["Category","Image","Title","Product_url","UPC", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "Availability", "Number of reviews"]
    return headers

def add_data_category(categories,soup,url):
    # add_data methods : data lists for csv file 
    for category in soup.find("ul",{"class":"breadcrumb"}).findAll("a")[2:]:
        return category.get_text()

def add_data_img(images,soup,url):
    parsed = urlparse(url)
    base_url = urlunparse(parsed)[:27]
    img_src = ""
    for img in soup.find("div",{"class":"col-sm-6"}).findAll("img"):
        img_src = base_url + img.get("src")[6:] 
        return img_src

def add_data_title(titles,soup,url):
    book_title = soup.find("div",{"class":"col-sm-6 product_main"}).find("h1").text.strip()
    return(book_title)

def add_data_table_values(values,soup,url):
    # loop into the list and get all the values from the table
    for value in soup.findAll("table",{"class":"table table-striped"}):
        for value_text in soup.findAll("td"):
            values.append(value_text.get_text())
    return values

# write everything in a csv file
def write_file(headers, values,csv_name):
    with open(csv_name, 'w',newline="", encoding="utf-8") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")
        headers = add_header_csv(headers)
        writer.writerow(headers)
        add_data_table_values(values,soup,url)
        writer.writerow(values)
    file.close()

if __name__ == "__main__":
    csv_headers = []
    csv_values = []
    csv_name = "book_scraped.csv"
    url = "https://books.toscrape.com/catalogue/worlds-elsewhere-journeys-around-shakespeares-globe_972/index.html"
    soup = website_access(url)
    csv_values.append(add_data_category(csv_values,soup,url))
    csv_values.append(add_data_img(csv_values,soup,url))
    csv_values.append(add_data_title(csv_values,soup,url))
    csv_values.append(add_data_product_page_url(csv_values,soup,url))
    write_file(csv_headers,csv_values,csv_name)
