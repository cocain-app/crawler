import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class BadProxyException(Exception):
    pass


def test_proxy(driver, proxy):
    try:
        driver.get("https://www.whatismyip.com/my-ip-information/")
        title = driver.title

        if(title == "My IP Information - WhatIsMyIP.com®"):
            return True
        else:
            return False
    except Exception as e:
        return False


def create_browser(headless=False, proxy=None, timeout=10, ublockpath=None):
    chrome_options = Options()
    if(headless):
        chrome_options.add_argument("--headless")
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

    if(proxy is not None):
        chrome_options.add_argument('--proxy-server=%s' % proxy)
        print("Browser using proxy server %s" % proxy)

    capabilities = DesiredCapabilities.CHROME
    capabilities['loggingPrefs'] = {'performance': 'ALL'}

    driver = webdriver.Chrome(
        options=chrome_options, desired_capabilities=capabilities)

    driver.set_page_load_timeout(timeout)
    driver.implicitly_wait(30)

    if(proxy is not None):
        if(test_proxy(driver, proxy)):
            return driver
        else:
            raise BadProxyException()
    else:
        return driver
