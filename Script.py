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


def website_access(URL):
    # url of the website to scrape
    # attempt to access the url, if req = 200 -> (success) 
    # instantiate a soup object with 2 parameters : the data content(can be text or other methods) needed and the type to parse  
    req = requests.get(URL)
    soup = bs(req.text, "html.parser")
    soup.prettify("utf-8")
    return soup

def add_data_product_page_url(product_url_list, soup,URL):
    # get current url
    soup = website_access(URL)
    req = urlopen(URL)
    return req.geturl()

def add_header_csv(header_list):
    # add_header method : header lists for csv file
    header_list = ["Category","Image","Title","Product_Url","UPC", "Product Type", "Price (excl. tax)", "Price (incl. tax)", "Tax", "Availability", "Number of reviews"]
    return header_list

def add_data_category(category_list,soup,URL):
    # add_data methods : data lists for csv file 
    soup = website_access(URL)
    for category in soup.find("ul",{"class":"breadcrumb"}).findAll("a")[2:]:
        return category.get_text()

def add_data_img(image_list,soup,URL):
    soup = website_access(URL)
    parsed = urlparse(URL)
    base_url = urlunparse(parsed)[:27]
    img_src = ""
    for img in soup.find("div",{"class":"col-sm-6"}).findAll("img"):
        img_src = base_url + img.get("src")[6:] 
        return img_src

def add_data_title(title_list,soup,URL):
    soup = website_access(URL)
    book_title = soup.find("div",{"class":"col-sm-6 product_main"}).find("h1").text.strip()
    return(book_title)

def add_data_table_values(value_list,soup,URL):
    soup = website_access(URL)
    # loop into the list and get all the values from the table
    for value in soup.findAll("table",{"class":"table table-striped"}):
        for value_text in soup.findAll("td"):
            value_list.append(value_text.get_text())
    return value_list

# write everything in a csv file
def write_file(header_list, value_list,csv_name):
    with open(csv_name, 'w',newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")
        header_list = add_header_csv(header_list)
        writer.writerow(header_list)
        add_data_table_values(value_list,soup,URL)
        writer.writerow(value_list)
    file.close()

if __name__ == "__main__":
    csv_headers = []
    csv_values = []
    csv_name = "book_scraped.csv"
    URL = "https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"
    soup = website_access(URL)
    csv_values.append(add_data_category(csv_values,soup,URL))
    csv_values.append(add_data_img(csv_values,soup,URL))
    csv_values.append(add_data_title(csv_values,soup,URL))
    csv_values.append(add_data_product_page_url(csv_values,soup,URL))
    write_file(csv_headers,csv_values,csv_name)
