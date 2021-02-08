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


def website_access():
    # url of the website to scrape
    URL = "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"
    # attempt to access the url, if req = 200 -> (success) 
    # instantiate a soup object with 2 parameters : the data content(can be text or other methods) needed and the type to parse  
    req = requests.get(URL)
    soup = bs(req.text, "html.parser")
    soup.prettify("utf-8")
    return soup

# cannot get anything different than ../../index.html, looking for get_current_url() function ?
def add_product_page_url(product_url_list, soup):
    soup = website_access()
    #req url response 

def add_header_product_url(header_list):
    return "Product_url"

def add_data_category(category_list,soup):
    soup = website_access()
    for category in soup.find("ul",{"class":"breadcrumb"}).findAll("a")[2:]:
        return category.get_text()

def add_header_category(header_list):
    return "Category"

def add_data_img(image_list,soup):
    soup = website_access()
    for img in soup.find("div",{"class":"col-sm-6"}).findAll("img"):
        return img.get("src")

def add_header_image(header_list):
    return "Image_url"

def add_data_title(title_list,soup):
    soup = website_access()
    book_title = soup.find("h1").text.strip()
    return(book_title)

def add_header_title(header_list):
    return "Title"


# would it be better to have a dictionnary to write csv ?
def write_file(header_list, value_list):
    # write everything in a csv file
    soup = website_access()
    with open('book_scraped.csv', 'w',newline="") as file:
        writer = csv.writer(file,delimiter=";")

        # loop into the list and get all the labels
        for header in soup.findAll("table",{"class":"table table-striped"}):
            for header_text in soup.findAll("th"):
                header_list.append(header_text.get_text())
            writer.writerow(header_list)

        # loop into the list and get all the values
        for value in soup.findAll("table",{"class":"table table-striped"}):
            for value_text in soup.findAll("td"):
                value_list.append(value_text.get_text())
            writer.writerow(value_list)
    file.close()

if __name__ == "__main__":
    csv_headers = []
    csv_values = []
    soup = website_access()
    csv_headers.append(add_header_category(csv_headers))
    csv_headers.append(add_header_image(csv_headers))
    csv_headers.append(add_header_title(csv_headers))
    csv_values.append(add_data_category(csv_values,soup))
    csv_values.append(add_data_img(csv_values,soup))
    csv_values.append(add_data_title(csv_values,soup))
    write_file(csv_headers,csv_values)
