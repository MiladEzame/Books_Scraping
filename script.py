from bs4 import BeautifulSoup as bs
import csv
import requests
import os
from urllib.request import urlopen
from urllib.parse import urlparse, urlunparse
import re

def website_access(url):
    """
        Requesting access to the website in parameter(url)
        Then retrieving its content through a beautiful soup object
    """
    req = requests.get(url)
    soup = bs(req.content, "html.parser")
    soup.prettify("utf-8")
    return soup

def add_data_product_page_url(soup, url):
    """
        Retrieves the current url by requesting through the geturl() 
        Method in the urlopen module
    """
    req = urlopen(url)
    return req.geturl()

def add_header_csv():
    """
        Returns all the headers in the form of a list 
        That list is going to be writter inside the write_file() method
    """
    headers = ["Category", "Image", "Product_description", "Title", 
    "Product_page_url", "Universal_ product_code (upc)", "Product Type", 
    "Price_excluding_tax", "Price_including_tax", "Tax", 
    "Number_available", "Number of reviews"]
    return headers

def add_data_category(soup):
    """
        Returns the category of the book inside the soup object 
    """
    for category in soup.find("ul", {"class": "breadcrumb"}).findAll("a")[2:]:
        return category.get_text()

def add_data_img(soup, url):
    """
        Returns the image url of the book inside the soup object
        Parsing url (with urlunparse/urlparse) and img src to get full url
    """
    parsed = urlparse(url)
    base_url = urlunparse((parsed.scheme, parsed.netloc, "/", None, None, None))
    img_src = ""
    for img in soup.find("div", {"class": "col-sm-6"}).findAll("img"):
        img_src = base_url + img.get("src")[6:] 
        return img_src

def add_data_title(soup):
    """
        Returns the title of the book inside the soup object
    """
    book_title = soup.find("div", {"class": "col-sm-6 product_main"}).find("h1").text.strip()
    return(book_title)

def add_data_table_values(values, soup):
    """
        Returns all the product information of the book in the soup object
    """
    for value in soup.findAll("table", {"class": "table table-striped"}):
        for value_text in soup.findAll("td"): 
            values.append(value_text.get_text())
    return values

def add_product_description(soup):
    """
        Returns the description of the book inside the soup object in 
        Using select because we need to get directly to the first child 
        paragraph (with >) inside the article.product_page
    """
    for item in soup.select("article.product_page > p"):
        description = item.text.strip()
    return description

def download_image(soup, url):
    """
        Saves the image of the book inside the soup object 
        Writes it inside a file with a .jpg extension
        Replace ":", "/" characters with replace() and using re module to 
        Replace all the other special characters with the sub() method
        Defined a limit of 25 chars because a long name file creates error
    """
    parsed = urlparse(url)
    base_url = urlunparse((parsed.scheme, parsed.netloc, "/", None, None, None))
    for image in soup.find("div", {"class": "col-sm-6"}).findAll("img"):
        name = image["alt"].replace(":", " ").replace("/", " ")[:25]
        re.sub("[^A-Za-z0-9]+", " ", name)
        print("Saving : {}".format(name))
        link = base_url + image.get("src")[6:] 
        with open(name + ".jpg", "ab") as f:
            img = requests.get(link)
            f.write(img.content)
    f.close()

def write_file(values, csv_name):
    """
        Writes all the headers and then writes all the values retrieved 
        Using all the methods used before
    """
    with open(csv_name, 'w', newline = "", encoding = "utf-8") as file:
        writer = csv.writer(file, delimiter = ";")
        headers = add_header_csv()
        writer.writerow(headers)
        add_data_table_values(values, soup)
        writer.writerow(values)
    file.close()

if __name__ == "__main__":
    """
        Create a soup object and request access to the url
        Retrieve its content - Create a values list in which
        We append all the data of the previous methods 
        Write all the values inside the list with the write_file method
    """
    csv_values = []
    csv_name = "book_scraped.csv"
    url = "https://books.toscrape.com/catalogue/red-hoodarsenal-vol-1-open-for-business-red-hoodarsenal-1_729/index.html"
    soup = website_access(url)
    download_image(soup, url)
    csv_values.append(add_data_category(soup))
    csv_values.append(add_data_img(soup, url))
    csv_values.append(add_product_description(soup))
    csv_values.append(add_data_title(soup))
    csv_values.append(add_data_product_page_url(soup, url))
    write_file(csv_values, csv_name)