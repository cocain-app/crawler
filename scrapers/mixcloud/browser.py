import time
import json


def get_mixcloud_set_source(driver, url, autocrawl=False):
    driver.get(url)

    time.sleep(2)

    # Click play
    driver.find_element_by_css_selector(
        ".play-button-wrap .play-button").click()

    # Get window calls
    calls = driver.get_log("performance")

    # Get tracklist
    for call in calls:
        message = json.loads(call["message"])["message"]
        if(message["method"] == "Network.responseReceived"):
            url = message["params"]["response"]["url"]
            print(url)
            if("https://www.mixcloud.com/tracklist/" in url):
                print(url)

    time.sleep(120)
