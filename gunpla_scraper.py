from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import random

gundam_data = {}
texts = []
h3_tags = ["Articulation", "Weapons/Other Gimmicks", "Customizing-based Tips"]
h2_tags = ["Includes", "Tips & Tricks", "Variants", "Notes & Trivia"]


driver = webdriver.Firefox()
driver.get(
    "https://breezewiki.com/gunpla/wiki/MG_MSN-06S-2_Sinanju_Stein_(Narrative_Ver.)_(Ver._Ka)"
)

side_profile = driver.find_elements(By.CSS_SELECTOR, "div.pi-item")

for item in side_profile:

    gundam_data[item.find_element(By.CSS_SELECTOR, "h3").text] = item.find_element(
        By.CSS_SELECTOR, "div.pi-data-value"
    ).text


def scrape_gallery_pics(gundam_data):
    gallery = driver.find_elements(By.CSS_SELECTOR, "div.wikia-gallery")

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

    gundam_data["images"] = real_images


def scrape_h2_tags(tags, gundam_data):

    for i, tag in enumerate(tags):

        test_pro = driver.find_element(
            By.XPATH,
            f"/html/body/div[2]/div[2]/main/div[2]/div/div/h2[{i+1}]/span[@class='mw-headline']",
        )

        # print(test_pro.text)
        if test_pro.text in tags:
            for sibling in range(1, 6):
                text_values = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[2]/div[2]/main/div[2]/div/div/h2[{i+1}]/following-sibling::*[{sibling}]",
                )
                reg = text_values.find_elements(By.CSS_SELECTOR, "li")
                if len(reg) != 0:
                    break

        gundam_data[tag] = list(
            map(
                lambda x: str.replace(str.replace(x.text, "\n", " - "), "...", ""),
                reg,
            )
        )


def scrape_h3_tags(tags, gundam_data):

    for i, tag in enumerate(tags):

        test_pro = driver.find_element(
            By.XPATH,
            f"/html/body/div[2]/div[2]/main/div[2]/div/div/h3[{i+1}]/span[@class='mw-headline']",
        )

        # print(test_pro.text)
        if test_pro.text in tags:
            for sibling in range(1, 6):
                text_values = driver.find_element(
                    By.XPATH,
                    f"/html/body/div[2]/div[2]/main/div[2]/div/div/h3[{i+1}]/following-sibling::*[{sibling}]",
                )
                reg = text_values.find_elements(By.CSS_SELECTOR, "li")
                if len(reg) != 0:
                    break

        gundam_data[tag] = list(
            map(
                lambda x: str.replace(str.replace(x.text, "\n", " - "), "...", ""),
                reg,
            )
        )


scrape_h2_tags(h2_tags, gundam_data)
scrape_h3_tags(h3_tags, gundam_data)
scrape_gallery_pics(gundam_data)
print(gundam_data)
# test_pro =

# text_pro = driver.find_elements(By.CSS_SELECTOR, "h3")

# for tx in text_pro:
#     print(tx.text)
# lists = test_pro.find_elements(By.CSS_SELECTOR, "li")
"""
    For text,
    - Everything in li should be a single sentence
    - After '...', then join the nested points with it
    - Each sentence combined should contain a . after it    
"""
