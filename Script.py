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
category not ok
review_rating ok
image_url ok
"""

# for multiple pages, change the number into a variable to increment 
# example with this url : https://books.toscrape.com/catalogue/category/books/sequential-art_5/page-[number_to_increment].html

# url of the website to scrape
URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"

# attempt to access the url, if req = 200 -> (success) 
# instantiate a soup object with 2 parameters : the data content(can be text or other methods) needed and the type to parse  
req = requests.get(URL)
soup = bs(req.text, "html.parser")
req = requests.get(URL)
soup = bs(req.text, "html.parser")
soup.prettify("utf-8")
csv_row1 = []
csv_row2 = []
# find the tags
book_title = soup.find("h1").text.strip()
image_url = soup.img["src"]
category = soup.find("ul",attrs={"class":"breadcrumb"}).find_all("a")[2:]

print(category)


csv_row1.append("Title")
csv_row1.append("Image_url")
csv_row1.append("Category")

csv_row2.append(book_title)
csv_row2.append(image_url)
csv_row2.append(category)



# write everything in a csv file
with open('book_scraped.csv', 'w',newline="") as file:
    writer = csv.writer(file)

    # loop into the list and get all the labels
    for header in soup.findAll("table"):
        for header_text in soup.findAll("th"):
            csv_row1.append(header_text.get_text())
        writer.writerow(csv_row1)

    # loop into the list and get all the values
    for value in soup.findAll("table"):
        for value_text in soup.findAll("td"):
            csv_row2.append(value_text.get_text())
        writer.writerow(csv_row2)

file.close()