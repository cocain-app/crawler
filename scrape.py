import sys
import time
from selenium import webdriver

from database import create_database_connection, upload_set
from scrapers import scrape_set

# Establish Database connection
try:
    conn = create_database_connection()
except Exception as e:
    print(e)
    sys.exit()

# Create browser
driver = webdriver.Chrome()
driver.implicitly_wait(30)

# Scrape tracks
with open('queue.txt') as f:
    for line in f:
        url = line.strip()

        if(url == ""):
            print("Please populate the queue.txt")
            sys.exit()

        print("Scraping %s:" % url)

        driver.get(url)
        html = driver.page_source

        setlist = scrape_set(html, url)
        upload_set(conn, setlist)

        time.sleep(5)

# Clear queue.txt & close browsers
print("Scraped queue.txt")
driver.quit()
open("queue.txt", 'w').close()
