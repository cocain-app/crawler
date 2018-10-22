import sys
import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from scrapers import scrape_set


def crawl(autocrawl=False, sleeptime=5, max=None, nodb=False, headless=False, queue=[]):

    if not nodb:
        # Additional imports
        from database import create_database_connection, upload_set

        # Establish Database connection
        try:
            conn = create_database_connection()
        except Exception as e:
            print(e)
            sys.exit()

    # Create browser
    chrome_options = Options()
    if(headless):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)

    # Scrape tracks
    urls = queue
    urls_scraped = set()
    while(len(urls) > 0):
        num_current = len(urls_scraped) + 1
        num_overall = str(len(urls) + len(urls_scraped)) + ("+" if autocrawl else "")

        # Exit if enough sets are scraped is reached
        if(max is not None and max < num_current):
            break

        print("Scraping url %s of %s" % (num_current, num_overall))

        url = urls[0]
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

        # Save the scraped information
        if not nodb:
            upload_set(conn, setlist)
        else:
            try:
                with open("output.json", "r+") as f:
                    data = json.load(f)
            except Exception as e:
                data = []

            data.append(setlist)

            with open("output.json", "w+") as f:
                f.write(json.dumps(data))

        # Add links to queue
        if(autocrawl):
            if(setlist["previous_set"]):
                url = setlist["previous_set"]
                if not (url in urls) and not (url in urls_scraped):
                    urls.append(url)
                    print("Added previous setlist %s to queue."
                          % setlist["previous_set"])

            if(setlist["next_set"]):
                url = setlist["next_set"]
                if not (url in urls) and not (url in urls_scraped):
                    urls.append(url)
                    print("Added next setlist %s to queue."
                          % setlist["next_set"])

            for link in setlist["artist_links"]:
                url = link
                if not (url in urls) and not (url in urls_scraped):
                    urls.append(url)
                    print("Added artist setlist %s to queue." % link)

            for link in setlist["related_links"]:
                url = link
                if not (url in urls) and not (url in urls_scraped):
                    urls.append(url)
                    print("Added related setlist %s to queue." % link)

        # Move url to already scraped
        urls_scraped.add(urls.pop(0))

        time.sleep(sleeptime)

    # Clear queue.txt & close browsers
    print("Scraped %s sets" % num_current)
    driver.quit()


if __name__ == "__main__":
    # Parse arguments
    parser = argparse.ArgumentParser()

    parser.add_argument("-a", "--autocrawl",
                        help="automatically add urls to queue",
                        action="store_true")
    parser.add_argument("-s", "--sleeptime", type=int)
    parser.add_argument("--max", type=int)
    parser.add_argument("--nodb",
                        help="disable the database connection and scrape to a file instead",
                        action="store_true")
    parser.add_argument("--headless",
                        help="run chrome in headless mode",
                        action="store_true")

    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument('--queuefile',
                        help="path to a txt file with links (one per line)")
    source.add_argument('--link',
                        help="first link to start scraping")

    args = parser.parse_args()

    if(args.autocrawl):
        autocrawl = True
        print("Automatic crawling is turned on")
    else:
        autocrawl = False

    if(args.sleeptime):
        if args.sleeptime > 4:
            sleeptime = args.sleeptime
            print("Sleeptime is set to %s" % sleeptime)
        else:
            sleeptime = 5
            print("Sleeptime needs to be a minimum of 5 seconds")
    else:
        sleeptime = 5

    if(args.max):
        if args.max > 0:
            max = args.sleeptime
            print("Maximum number of sets is set to %s" % max)
        else:
            max = None
            print("Maximum number of sets needs to be positive")
    else:
        max = None

    if(args.nodb):
        nodb = True
    else:
        nodb = False

    if(args.headless):
        headless = True
    else:
        headless = False

    queue = []
    if(args.queuefile):
        with open(args.queuefile) as f:
            for line in f:
                queue.append(line.strip())
    elif(args.link):
        queue.append(args.link)

    # Crawl
    crawl(autocrawl=autocrawl, sleeptime=sleeptime, nodb=nodb, headless=headless, queue=queue, max=max)

    # Clear queue
    if args.queuefile:
        open("queue.txt", 'w').close()
