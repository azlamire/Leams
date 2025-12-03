import json
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


# TODO: Make with playwright cause I need a asyncio for fastapi and production
def get_category_images():
    driver = uc.Chrome()
    driver.get("https://www.twitch.tv/directory")
    time.sleep(10)
    # TODO: Make it workable in playwright
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    divs = driver.find_elements(By.XPATH, '//div[@class="Layout-sc-1xcs6mc-0 fNsrnJ"]')
    y = dict()
    for link in divs:
        imgs = link.find_element(By.XPATH, './/img[@class="tw-image"]')
        src = imgs.get_attribute("src")
        print(src)
        name = link.find_element(
            By.XPATH, './/h2[@class="CoreText-sc-1txzju1-0 erESIP"]'
        )
        test = name.text
        y[test] = src
    with open("app/category.json", "w") as category:
        json.dump(y, category, indent=4)

    driver.quit()


if __name__ == "__main__":
    get_category_images()
