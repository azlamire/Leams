# NOTE: This model is just for demonsstratino what would see an user
import json
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


# TODO: Make with playwright cause I need a asyncio for fastapi and production
def get_streams_images():
    print("HI")
    driver = uc.Chrome()
    driver.get("https://www.twitch.tv")
    time.sleep(10)
    # TODO: Make it workable in playwright
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    divs = driver.find_elements(
        By.XPATH, '//article[@class="Layout-sc-1xcs6mc-0 ghbJdj"]'
    )
    y = dict()
    for link in divs:
        img = link.find_element(By.XPATH, './/img[@class="tw-image"]')
        title = link.find_element(
            By.XPATH, './/h4[@class="CoreText-sc-1txzju1-0 kVxrzL"]'
        )
        avatar = link.find_element(
            By.XPATH,
            './/img[@class="InjectLayout-sc-1i43xsx-0 fAYJcN tw-image tw-image-avatar"]',
        )
        name = link.find_element(
            By.XPATH,
            './/p[@class="CoreText-sc-1txzju1-0 kdDAY"]',
        )
        avatar = avatar.get_attribute("src")
        img = img.get_attribute("src")
        title = title.text
        name = name.text

        y[title] = [avatar, img, name]
    print(y)
    with open("app/main.json", "w") as category:
        json.dump(y, category, indent=4)

    driver.quit()


if __name__ == "__main__":
    get_streams_images()
