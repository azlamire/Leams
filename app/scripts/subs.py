# NOTE: This model is just for demonsstratino what would see an user
import json
import time
from selenium.webdriver.common.by import By
import undetected_chromedriver as uc


# TODO: Make with playwright cause I need a asyncio for fastapi and production
def get_subs():
    print("HI")
    driver = uc.Chrome()
    driver.get("https://www.twitch.tv")
    time.sleep(50)
    # TODO: Make it workable in playwright
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    subs = driver.find_elements(
        By.XPATH,
        '//a[@class="ScCoreLink-sc-16kq0mq-0 fytYW InjectLayout-sc-1i43xsx-0 cnzybN side-nav-card__link tw-link"]',
    )
    y = dict()
    for link in subs:
        try:
            nickname = link.find_element(
                By.XPATH,
                './/p[@class="CoreText-sc-1txzju1-0 dTdgXA InjectLayout-sc-1i43xsx-0 hnBAak"]',
            )
            kind = link.find_element(
                By.XPATH, './/p[@class="CoreText-sc-1txzju1-0 iMyVXK"]'
            )
            avatar = link.find_element(
                By.XPATH,
                './/img[@class="InjectLayout-sc-1i43xsx-0 fAYJcN tw-image tw-image-avatar"]',
            )
            kind = kind.text
            print(kind)
            nickname = nickname.text
            print(nickname)
            avatar = avatar.get_attribute("src")
            print(avatar)

            y[nickname] = [avatar, kind]
        except:
            continue
    with open("app/subs.json", "w") as category:
        json.dump(y, category, indent=4)
    driver.quit()


if __name__ == "__main__":
    get_subs()
