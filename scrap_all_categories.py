import scrap_category
import os
from urllib.parse import urlparse, urlunparse


def navigate_all_categories(soup, url):
    """
        Navigating inside the Category navigation bar
        Returning the list of all the categories present inside the bar
    """
    parsed = urlparse(url)
    base_url = urlunparse((parsed.scheme, parsed.netloc, "/", None, None, None))
    navigation = soup.find("ul", {"class": "nav nav-list"})
    categories_url = []
    for categories in navigation.find("ul").findAll("li"):
        for category_text in categories.findAll("a"):
            category_value = category_text.get("href")
            final_url = base_url + category_value
            scrap_category.category_website_access(final_url)
            categories_url.append(final_url)
    return categories_url


def get_category_names(soup):
    """
        Parsing the url and retrieving all the category names
        Names will be used to form the csv_files
    """
    navigation = soup.find("ul", {"class": "nav nav-list"})
    category_names = []
    for categories in navigation.find("ul").findAll("li"):
        for category_text in categories.findAll("a"):
            category_value = category_text.text.strip()
            category_names.append(category_value)
    return category_names


def csv_cat_by_name(soup):
    """
        Using the names from the returned value in get_category_names()
        Creating csv files for each category scraped
    """
    categories = get_category_names(soup)
    csv_names = []
    for names in categories:
        csv_by_category = names + "_scraped.csv"
        csv_names.append(csv_by_category)
    return csv_names


def scrape_books_from_all_categories(soup, url, folder):
    """
        Creating a list of all the urls inside the navigation bar
        Creating a list of all the csv names returned in csv_cat_by_name()
        Using zip() to iterate on url and csv_names at the same time
        Otherwise the loops wouldn't work properly
        Same process as used in scrap_category, accessing the soup object
        To avoid writing inside the folder, we use os.chdir to save
        The images inside the folder and go back to parent folder to
        Create all the csv_files of each categories
    """
    all_urls = navigate_all_categories(soup, url)
    csv_names = csv_cat_by_name(soup)
    for url, csv_name in zip(all_urls, csv_names):
        soup = scrap_category.category_website_access(url)
        os.chdir("..")
        scrap_category.write_csv_headers(csv_name)
        os.chdir(folder)
        scrap_category.scrape_all_books_one_category(soup, url, csv_name, folder)


if __name__ == "__main__":
    """
        Accessing and getting the content of the main page
        Create a folder and scrape from all categories
        The csv files are created inside the method itself
    """
    url = "https://books.toscrape.com/index.html"
    soup = scrap_category.category_website_access(url)
    folder = "images_saved"
    scrap_category.create_directory(folder)
    scrape_books_from_all_categories(soup, url, folder)
