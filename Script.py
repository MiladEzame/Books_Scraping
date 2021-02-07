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
URL = "https://books.toscrape.com/catalogue/sharp-objects_997/index.html"

# attempt to access the url, if req = 200 -> (success) 
# instantiate a soup object with 2 parameters : the data content(can be text or other methods) needed and the type to parse  
req = requests.get(URL)
soup = bs(req.text, "html.parser")
soup.prettify("utf-8")
# still cannot write properly £ into the csv file

# cannot get anything different than ../../index.html, looking for get_current_url() function ?
def add_current_url():
    current_url = soup.find("div",{"class":"col-sm-8 h1"}).find("a").get("href")
    #url_list.append(current_url)
    #header_list.append("Current_Url")
    print(current_url)

def add_data_category(category_list,header_list):
    for categories in soup.findAll("ul",{"class":"breadcrumb"}):
        for category in soup.findAll("a")[3:]:
            category_list.append(category.get_text())
    header_list.append("Category")

def add_data_img(image_list,header_list):
    image_url = soup.img["src"]
    image_list.append(image_url)
    header_list.append("Image_url")

def add_data_title(title_list,header_list):
    book_title = soup.find("h1").text.strip()
    title_list.append(book_title)
    header_list.append("Title")

def write_file(header_list, value_list):
    # write everything in a csv file
    add_data_category(csv_values,csv_headers)
    add_data_img(csv_values,csv_headers)
    add_data_title(csv_values,csv_headers)
    with open('book_scraped.csv', 'w',newline="") as file:
        writer = csv.writer(file)

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

write_file(csv_headers,csv_values)
