from selenium_driverless.types.by import By
import asyncio, json, os

async def allCategories(driver):
    categories = await driver.find_elements(By.XPATH, '//div[@class="game-card"]')
    json_categrories = dict()
    for category, number in enumerate(categories):
        img = await category.find_element(By.TAG_NAME, 'img')
        json_categrories[number] = img.get_attribute('src')
    with open(os.path.abspath(""), 'w') as file:
        file.write(json.dumps(json_categrories))

                
