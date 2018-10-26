import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException


class BadProxyException(Exception):
    pass


def test_proxy(driver, proxy):
    driver.get("https://www.whatismyip.com/my-ip-information/")

    try:
        ip_add = driver.find_element_by_id("ip-version-check").text
        ip_add = ip_add.replace("Your IPv4 is: ", "")
        print(ip_add)

        if(ip_add == proxy.split(":")[0]):
            return True
        else:
            return False
    except NoSuchElementException as e:
        return False


def create_browser(headless=False, proxy=None, timeout=10):
    chrome_options = Options()
    if(headless):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

    if(proxy is not None):
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        print("Browser using proxy server %s" % proxy)

    driver = webdriver.Chrome(options=chrome_options)
    driver.set_page_load_timeout(timeout)
    driver.implicitly_wait(30)

    if(proxy is not None):
        if(test_proxy(driver, proxy)):
            return driver
        else:
            raise BadProxyException()
    else:
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
