from bs4 import BeautifulSoup as bs
import csv
import requests
from urllib.request import urlopen

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

def add_header_csv(header_list,URL):
    # add_header method : header lists for csv file
    header_list.append("Category")
    header_list.append("Image")
    header_list.append("Title")
    header_list.append("Product_Url")

def add_data_category(category_list,soup,URL):
    # add_data methods : data lists for csv file 
    soup = website_access(URL)
    for category in soup.find("ul",{"class":"breadcrumb"}).findAll("a")[2:]:
        return category.get_text()

def add_data_img(image_list,soup,URL):
    soup = website_access(URL)
    for img in soup.find("div",{"class":"col-sm-6"}).findAll("img"):
        return img.get("src")

def add_data_title(title_list,soup,URL):
    soup = website_access(URL)
    book_title = soup.find("div",{"class":"col-sm-6 product_main"}).find("h1").text.strip()
    return(book_title)

# write everything in a csv file
def write_file(header_list, value_list,soup,URL):

    soup = website_access(URL)
    with open('book_scraped.csv', 'w',newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")

        # loop into the list and get all the headers
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
    URL = "https://books.toscrape.com/catalogue/the-dirty-little-secrets-of-getting-your-dream-job_994/index.html"
    soup = website_access(URL)
    add_header_csv(csv_headers,URL)
    csv_values.append(add_data_category(csv_values,soup,URL))
    csv_values.append(add_data_img(csv_values,soup,URL))
    csv_values.append(add_data_title(csv_values,soup,URL))
    csv_values.append(add_data_product_page_url(csv_values,soup,URL))
    write_file(csv_headers,csv_values,soup,URL)