from selenium_driverless.types.by import By
from selenium_driverless import webdriver
from constants import COMPLETED
import asyncio, json, os, sys, time


async def products():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("--fullscreen")
    async with webdriver.Chrome(options=options) as driver:
        id = sys.argv[1]
        url = "https://www.dns-shop.ru/product/" + id 
        await driver.get(url)
        time.sleep(20)
        ready_state = ''
        while ready_state != COMPLETED:
            ready_state = await driver.execute_script("return document.readyState")
            await asyncio.sleep(0.1)
        product_name = await driver.find_element(By.XPATH, '//h1[@class="product-card-top__title"]')
        params = {
            "id": id,
            "product_name": await product_name.text
        }
        print(json.dumps(params, ensure_ascii=False))


asyncio.run(products())

