from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import random

options = Options()
options.add_argument("--headless")
options.set_preference(
    "general.useragent.override",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
)
options.add_argument("--disable-gpu")

driver = webdriver.Firefox(options=options)

links = [
    "https://gunpla.fandom.com/wiki/Master_Grade",
    "https://gunpla.fandom.com/wiki/Real_Grade",
    "https://gunpla.fandom.com/wiki/High_Grade_Universal_Century",
    "https://gunpla.fandom.com/wiki/High_Grade_Gundam_Thunderbolt",
    "https://gunpla.fandom.com/wiki/High_Grade_Gundam_The_Origin",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_SEED",
    "https://gunpla.fandom.com/wiki/High_Grade_Cosmic_Era",
    "https://gunpla.fandom.com/wiki/High_Grade_Gundam_SEED",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_00",
    "https://gunpla.fandom.com/wiki/Gundam_Reconguista_in_G",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_IRON-BLOODED_ORPHANS",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam:_The_Witch_from_Mercury",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_GQuuuuuuX",
    "https://gunpla.fandom.com/wiki/Gundam:_Requiem_for_Vengeance",
    "https://gunpla.fandom.com/wiki/Gundam_Build_Metaverse",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_SEED_Freedom",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam:_Cucuruz_Doan%27s_Island",
    "https://gunpla.fandom.com/wiki/Gundam_Build_Divers",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_Thunderbolt",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam:_The_Origin",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_AGE",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_Unicorn",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_SEED_C.E._73:_STARGAZER",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_SEED_Destiny",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam:_The_08th_MS_Team",
    "https://gunpla.fandom.com/wiki/New_Mobile_Report_Gundam_Wing",
    "https://gunpla.fandom.com/wiki/Mobile_Fighter_G_Gundam",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Victory_Gundam",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_0083:_Stardust_Memory",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_F91",
    "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_0080:_War_in_the_Pocket",
    # "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam:_Char%27s_Counterattack",
    # "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam_ZZ",
    # "https://gunpla.fandom.com/wiki/Mobile_Suit_Zeta_Gundam",
    # "https://gunpla.fandom.com/wiki/Mobile_Suit_Gundam",
]


def img_link_scraper(url):

    time.sleep(random.randint(5, 7))
    print(url)
    driver.get(url)

    colls = driver.find_elements(By.CSS_SELECTOR, ".wikia-gallery-item")
    return list(
        map(
            lambda x: x.find_element(By.CSS_SELECTOR, "a").get_attribute("href") + "\n",
            colls,
        )
    )


gunpla_links = []

for link in links:
    gunpla_links.extend(img_link_scraper(link))

with open("gunpla_links.txt", "w+") as file:
    file.writelines(gunpla_links)
