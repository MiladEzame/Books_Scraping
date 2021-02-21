from bs4 import BeautifulSoup as bs
import csv
import requests
import script
import os
from urllib.parse import urlparse, urlunparse

def category_website_access(url):
    req = requests.get(url)
    soup = bs(req.content,"html.parser")
    soup.prettify("utf-8")
    return soup

# gets the book url and return a list of urls to be called in scrape data from product page method
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
        urls_books.append(final_url)
    return urls_books

# navigate multiple pages and retrieve the data from each books in each page
def scrape_all_books_one_category(soup, url, csv_name, folder):
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
            scrape_data_from_product_page(soup, next_url, csv_name, folder)
        else:
            next_url = base_url + "index.html" 
            req = requests.get(next_url) 
            soup = bs(req.content,"html.parser")
            scrape_data_from_product_page(soup, next_url, csv_name)
            break

# call all the functions from previous script
def scrape_data_from_product_page(soup, url, csv_name, folder):
    urls_books = navigate_books_single_page(soup, url)   
    for urls in urls_books:
        values = []
        soup = category_website_access(urls)
        script.download_image(soup,urls)
        os.chdir("..")
        values.append(script.add_data_category(soup,urls))
        values.append(script.add_data_img(soup, urls))
        values.append(script.add_product_description(soup))
        values.append(script.add_data_title(soup, urls))
        values.append(script.add_data_product_page_url(soup, urls))
        for value_text in soup.findAll("td"):
            values.append(value_text.get_text())
        write_csv_values(values, csv_name)
        os.chdir(folder)

def create_directory(folder):
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
        os.chdir(os.path.join(os.getcwd(), folder))
    except:
        os.chdir(os.path.join(os.getcwd(), folder))

def scrape_images_from_pages(soup, urls_books):
    for url in urls_books:
        images = []
        soup = category_website_access(url)
        images.append(script.add_data_img(soup, url))
        write_csv_images(images)        

def write_csv_headers(csv_name):
    with open(csv_name, 'w', encoding='utf-8', newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        headers = []
        headers = script.add_header_csv(headers)
        writer = csv.writer(file,delimiter=";")
        writer.writerow(headers)
    file.close()

"""
def write_csv_image_header():
    with open("images.csv", 'w', encoding='utf-8') as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file, delimiter = "\n")
        header = ["All images saved"]
        writer.writerow(header)
    file.close()
"""

def write_csv_values(values, csv_name):
    with open(csv_name, 'a', encoding='utf-8', newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")
        writer.writerow(values)
        file.close()
        
"""
def write_csv_images(values):
    with open("images.csv", 'a', encoding='utf-8', newline="") as file:
        # create a writer and assign the delimiter as ";" because of the french delimiter of csv files in excel
        writer = csv.writer(file,delimiter=";")
        writer.writerow(values)
        file.close()
"""

if __name__ == "__main__":
    url = "https://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    # argparse 
    csv_name = "books_one_category_scraped.csv"
    folder = "Images_Saved"
    soup = category_website_access(url)
    #write_csv_image_header()
    write_csv_headers(csv_name)
    create_directory(folder)
    scrape_all_books_one_category(soup, url, csv_name, folder)
