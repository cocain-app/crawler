def get_tracklist_set_source(driver, url, autocrawl=False):
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
