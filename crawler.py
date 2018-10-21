import sys
import time
import argparse
from selenium import webdriver

from database import create_database_connection, upload_set
from scrapers import scrape_set


def crawl(autocrawl=False, sleeptime=5):
    # Establish Database connection
    try:
        conn = create_database_connection()
    except Exception as e:
        print(e)
        sys.exit()

    # Create browser
    driver = webdriver.Chrome()
    driver.implicitly_wait(30)

    # Load queue
    urls = []
    with open('queue.txt') as f:
        for line in f:
            urls.append(line.strip())

    # Scrape tracks
    for url in urls:
        if(url == "" or url is None):
            continue

        print("Scraping %s:" % url)
        driver.get(url)

        # Expand sidebar links
        if(autocrawl):
            for element in driver.find_elements_by_css_selector(
                "a.list-group-item:first-of-type"
            )[:2]:
                driver.execute_script("arguments[0].click();", element)

            time.sleep(2)

        html = driver.page_source
        setlist = scrape_set(html, url)
        # upload_set(conn, setlist)

        # Add links to queue
        if(autocrawl):
            if(setlist["previous_set"]):
                urls.append(setlist["previous_set"])
                print("Added previous setlist %s to queue."
                      % setlist["previous_set"])

            if(setlist["next_set"]):
                urls.append(setlist["next_set"])
                print("Added next setlist %s to queue." % setlist["next_set"])

            for link in setlist["artist_links"]:
                urls.append(link)
                print("Added artist setlist %s to queue." % link)

            for link in setlist["related_links"]:
                urls.append(link)
                print("Added related setlist %s to queue." % link)

        time.sleep(sleeptime)

    # Clear queue.txt & close browsers
    print("Scraped queue.txt")
    driver.quit()
    open("queue.txt", 'w').close()


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--autocrawl",
                        help="automatically add urls to queue",
                        action="store_true")

    parser.add_argument("-s", "--sleeptime", type=int)

    args = parser.parse_args()

    if(args.autocrawl):
        autocrawl = True
        print("Automatic crawling is turned on")
    else:
        autocrawl = False

    if(args.sleeptime):
        if args.sleeptime > 5:
            sleeptime = args.sleeptime
            print("Sleeptime is set to %s" % sleeptime)
        else:
            print("Sleeptime needs to be a minimum of 5 seconds")
    else:
        sleeptime = 5

    # Crawl
    crawl(autocrawl=autocrawl, sleeptime=sleeptime)
