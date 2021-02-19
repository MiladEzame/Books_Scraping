from bs4 import BeautifulSoup as bs
import csv
import requests
import script
import script_category
from urllib.parse import urlparse, urlunparse

def navigate_all_categories(soup, url):
    parsed = urlparse(url)
    base_url = parsed.scheme + "://" + parsed.netloc + "/" 
    navigation = soup.find("ul",{"class":"nav nav-list"})
    categories_url = []
    for categories in navigation.find("ul").findAll("li"):
        for category_text in categories.findAll("a"):
            category_value = category_text.get("href")
            final_url = base_url + category_value
            script_category.category_website_access(final_url)
            categories_url.append(final_url)
    return categories_url

def get_category_names(soup, url):
    parsed = urlparse(url)
    base_url = parsed.scheme + "://" + parsed.netloc + "/" 
    navigation = soup.find("ul",{"class":"nav nav-list"})
    category_names = []
    for categories in navigation.find("ul").findAll("li"):
        for category_text in categories.findAll("a"):
            category_value = category_text.text.strip()
            category_names.append(category_value)
    return category_names

def csv_category_by_name(soup, url):
    categories = get_category_names(soup, url)
    csv_names = []
    for names in categories:
        names.replace(" ", "_")
        csv_by_category = names + "_scraped.csv"
        csv_names.append(csv_by_category)
    return csv_names

def scrape_books_from_all_categories(soup, url):
    all_urls = navigate_all_categories(soup, url)
    csv_names = csv_category_by_name(soup, url)
    for url,csv_name in zip(all_urls, csv_names):
        script_category.write_csv_headers(csv_name)
        script_category.scrape_all_books_one_category(soup, url, csv_name)

if __name__ == "__main__":
    url = "https://books.toscrape.com/index.html"
    soup = script_category.category_website_access(url)
    csv_names = csv_category_by_name(soup, url)
    #navigate_all_categories(soup, url)
    script_category.write_csv_image_header()
    scrape_books_from_all_categories(soup, url)
