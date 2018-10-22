import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def create_browser(headless=False):
    chrome_options = Options()
    if(headless):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(30)

    return driver


def get_page_source(driver, url, autocrawl=False):
    driver.get(url)

    # Expand sidebar links
    if(autocrawl):
        for element in driver.find_elements_by_css_selector(
            "a.list-group-item:first-of-type"
        )[:2]:
            driver.execute_script("arguments[0].click();", element)

        time.sleep(2)

    html = driver.page_source

    return html
