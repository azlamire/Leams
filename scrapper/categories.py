from selenium_driverless.types.by import By
import asyncio, json, os

async def allCategories(driver):
    categories = await driver.find_elements(By.XPATH, '//div[@class="game-card"]')
    arr_cat = dict()
    for number, category in enumerate(categories, start=1):
        img = await category.find_element(By.TAG_NAME, 'img')
        arr_cat[number] = await img.get_attribute('src')
    with open(os.path.abspath(f'../backend/data/categories.json'),'w') as file:
        file.write(json.dumps(arr_cat, indent=4, ensure_ascii=False))
       
