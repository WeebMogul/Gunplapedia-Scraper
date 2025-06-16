from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import time
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import logging
from tqdm import tqdm

# options.add_argument("--disable-gpu")

# Track scraping data success / failures
logging.basicConfig(
    filename="gunpla.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def scrape_gunpla_prod_data(url):

    options = Options()
    options.add_argument("--headless")
    options.set_preference(
        "general.useragent.override",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    )
    driver = webdriver.Firefox(options=options)

    gunpla_data = {}

    try:
        driver.get(url)
        time.sleep(3)

        title = driver.find_element(By.CSS_SELECTOR, "h1#firstHeading").text
        logging.info(f"Title: {title}")
        logging.info(f"URL: {url}")

        gunpla_data["URL"] = url
        # 📋 Scrape infobox key–value pairs
        infobox = driver.find_element(By.CSS_SELECTOR, "aside.portable-infobox")
        entries = infobox.find_elements(By.CSS_SELECTOR, ".pi-item")
        # print("\nInfobox entries:")
        for entry in entries:
            # Fields often come as label + value
            label_elems = entry.find_elements(By.CSS_SELECTOR, ".pi-data-label")
            value_elems = entry.find_elements(By.CSS_SELECTOR, ".pi-data-value")
            if label_elems and value_elems:
                label = label_elems[0].text.strip()
                value = value_elems[0].text.strip()
                gunpla_data[label] = value

        h2_tags = ["Includes", "Tips_&_Tricks", "Variants", "Notes_&_Trivia"]
        h3_tags = [
            "Articulation",
            "Weapons/Other_Gimmicks",
            "Customizing-based_Tips",
            "B-Club_related_customizations",
        ]

        for tags in h2_tags:
            try:
                heading = driver.find_element(By.XPATH, f"//h2[span[@id='{tags}']]")
                heading_text = heading.find_element(By.XPATH, "following-sibling::*[1]")

            except Exception:
                continue
            finally:
                gunpla_data[heading.text] = str.replace(
                    str.replace(heading_text.text.strip(), "\n", " - "),
                    "...",
                    "",
                )

        for tags in h3_tags:
            try:
                heading = driver.find_element(By.XPATH, f"//h3[span[@id='{tags}']]")
                heading_text = heading.find_element(By.XPATH, "following-sibling::*[1]")

            except Exception:
                continue
            finally:
                gunpla_data[heading.text] = str.replace(
                    str.replace(heading_text.text.strip(), "\n", " - "),
                    "...",
                    "",
                )

        # gather image links from the gallery
        gallery = driver.find_elements(By.CSS_SELECTOR, ".wikia-gallery")

        images = []
        real_images = []

        for picture in gallery:
            gallery_files = picture.find_elements(By.CSS_SELECTOR, "a.image")
            images.extend(list(map(lambda x: x.get_attribute("href"), gallery_files)))

        for image in images:
            driver.get(image)
            real_images.append(
                driver.find_element(By.CSS_SELECTOR, "div.page")
                .find_element(By.CSS_SELECTOR, "img")
                .get_attribute("src")
            )
            time.sleep(random.randint(1, 4))

        gunpla_data["image_data"] = real_images
        logging.info(f"Successfully retrieved {url}")
    except Exception:
        logging.error(f"Successfully retrieved {url}")
        driver.quit()
        return []
    finally:
        driver.quit()
        return gunpla_data


if __name__ == "__main__":

    sample_url = "https://breezewiki.nadeko.net/gunpla/wiki/HGRFV_RX-78(G)E_Gundam_EX"

    sample_data = scrape_gunpla_prod_data(sample_url)
    # scrape_gunpla_prod_data()
