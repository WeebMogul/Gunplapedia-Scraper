from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException

options = Options()
options.add_argument("--headless")
options.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
)
options.add_argument("--disable-gpu")

driver = webdriver.Firefox(options=options)


def table_scraper(url):
    driver.get(url)

    tables = driver.find_element(By.CSS_SELECTOR, ".tabber.wds-tabber")

    gunpla_table = tables.find_elements(By.CSS_SELECTOR, ".wds-tab__content")

    gundam_links = []

    for table in gunpla_table:
        links = table.find_elements(
            By.CSS_SELECTOR,
            "div.table-scroller > table.wikitable > tbody > tr > td > a[href]",
        )
        gundam_links.extend(links)

    return list(set(map(lambda x: x.get_attribute("href"), gundam_links)))


def img_link_scraper(url):
    driver.get(url)

    colls = driver.find_elements(By.CSS_SELECTOR, "div.wikia-gallery-item")

    return list(
        map(
            lambda x: x.find_element(By.CSS_SELECTOR, "a.image").get_attribute("href"),
            colls,
        )
    )


# links = table_scraper(
#     url="https://breezewiki.com/gunpla/wiki/High_Grade_IRON-BLOODED_ORPHANS"
# )

img_link_scraper(
    url="https://breezewiki.com/gunpla/wiki/Mobile_Suit_Gundam:_The_Witch_from_Mercury"
)
