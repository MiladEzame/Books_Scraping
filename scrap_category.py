from bs4 import BeautifulSoup as bs
import csv
import requests
import scrap_page
import os
from urllib.parse import urlparse, urlunparse


def category_website_access(url):
    """
        Requesting access to the website in parameter(url)
        Then retrieving its content through a beautiful soup object
    """
    req = requests.get(url)
    soup = bs(req.content, "html.parser")
    soup.prettify("utf-8")
    return soup


def navigate_books_single_page(soup, url):
    """
        Navigates inside the book category page, gets all the books links
    """
    parsed = urlparse(url)
    base_url = urlunparse((parsed.scheme, parsed.netloc, parsed.path.split("/")[1], None, None, None))
    book_url = ""
    urls_books = []
    for books in soup.find("ol", {"class": "row"}).findAll("a")[::2]:
        books_src = books.get("href")
        book_url = books_src[9:]
        final_url = base_url + "/" + book_url
        urls_books.append(final_url)
    return urls_books


def scrape_data_from_product_page(soup, url, csv_name, folder):
    """
        Repeats the whole process inside the scrap_page.py file
        Retrieves and writes all the information into a csv file
        Using "os.chdir(folder)" to write inside the images saved folder
        Using "os.chdir("..")" to come back to the parent folder
        This allows to write inside the csv file and not inside the folder
    """
    urls_books = navigate_books_single_page(soup, url)
    for urls in urls_books:
        values = []
        soup = category_website_access(urls)
        scrap_page.download_image(soup, urls)
        os.chdir("..")
        values.append(scrap_page.add_data_category(soup))
        values.append(scrap_page.add_data_img(soup, urls))
        values.append(scrap_page.add_product_description(soup))
        values.append(scrap_page.add_data_title(soup))
        values.append(urls)
        for value_text in soup.findAll("td"):
            values.append(value_text.get_text())
        write_csv_values(values, csv_name)
        os.chdir(folder)


def scrape_all_books_one_category(soup, url, csv_name, folder):
    """
        Looking for the number of pages inside the condition
        Using max_page to define the number of iteration inside for loop
        Inside the range, navigate from page 1 to X 
        If we can access that page then call the scrape_data method
        If not then we define a new url with index to avoid request errors
        Then we call the scrape_data_from_product_page() method
    """
    if soup.find("li", {"class": "current"}):
        next_page = soup.find("li", {"class": "current"}).text.strip()
        next_page = next_page.split(" ")
        max_page = int(next_page[-1])
    else: 
        max_page = 1
    parsed = urlparse(url)
    path = os.path.split(parsed.path)
    base_url = urlunparse((parsed.scheme, parsed.netloc, path[0], None, None, None))
    for page in range(1, max_page+1):
        next_url = base_url + "/page-{}.html".format(page)
        req = requests.get(next_url)    
        soup = bs(req.content, "html.parser")
        if req.status_code == 200:
            scrape_data_from_product_page(soup, next_url, csv_name, folder)
        else:
            next_url = base_url + "/index.html"
            req = requests.get(next_url) 
            soup = bs(req.content, "html.parser")
            scrape_data_from_product_page(soup, next_url, csv_name, folder)
            break


def create_directory(folder):
    """
        Create the directory inside which the images will be saved
        If we can access it then we get inside the folder
        If it already exists then we just get inside it
    """
    try:
        os.mkdir(os.path.join(os.getcwd(), folder))
        os.chdir(os.path.join(os.getcwd(), folder))
    except FileExistsError:
        os.chdir(os.path.join(os.getcwd(), folder))


def write_csv_headers(csv_name):
    """
        Writing all the headers into the csv file
    """
    with open(csv_name, 'w', encoding='utf-8', newline="") as file:
        headers = scrap_page.add_header_csv()
        writer = csv.writer(file, delimiter=";")
        writer.writerow(headers)
    file.close()


def write_csv_values(values, csv_name):
    """
        Writing all the values inside the csv file
    """
    with open(csv_name, 'a', encoding='utf-8', newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(values)
        file.close()
