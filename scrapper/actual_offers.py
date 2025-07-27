from selenium_driverless.types.by import By
import asyncio, json, os

async def actual_offers(driver):
    actual = await driver.find_elements(By.XPATH, '//div[@class="actual-offers__section"]')
    params = dict()
    index = 0
    for element in actual:
        print(element)
        try:
            img = await element.find_element(By.TAG_NAME, 'img')
            links = await element.find_elements(By.TAG_NAME, 'a')
            categories = [link for link in links[2:]]
            sub_params = dict()
            sub_params["name"] = await links[0].get_attribute('text')
            sub_params["name_link"] = await links[0].get_attribute('href')
            sub_params["img"] = await img.get_attribute('src')
            sub_params["img_link"] = await links[1].get_attribute('href')
            sub_params["categories"] = [await link.get_attribute('href') for link in categories]
            sub_params["categories_name"] = [await link.get_attribute('text') for link in categories]
            index += 1
            params[index] = sub_params
        except:
            continue
    with open(os.path.abspath(f'client/src/assets/files/actual-offers.json'),'w') as file:
        file.write(json.dumps(params, indent=4, ensure_ascii=False))
                