from selenium_driverless.types.by import By
import asyncio, json, os
async def products(driver):
    products = await driver.find_elements(By.CLASS_NAME, 'action-slide base-ui-slider__custom-slide-size_zDe base-ui-slider__slide-item_a4N')
    params = dict()
    index = 0
    for product in products:
        try:
            spans = await product.find_elements(By.TAG_NAME, 'span')
            links = await product.find_elements(By.TAG_NAME, 'a')
            img = await product.find_element(By.TAG_NAME, 'img')
            spans_text = [await span.text for span in spans]
            if len(spans_text) == 4:
                del spans_text[1]
            if spans_text[1] == spans_text[2]:
                spans_text[2] = 'none'
            sub_params = dict()
            sub_params["sale"] =  spans_text[0]
            sub_params["product_link"] = await links[0].get_attribute('href')
            sub_params["product_name"] = await links[0].get_attribute('text')
            sub_params["price"] = spans_text[1]
            sub_params["old_price"] = spans_text[2]
            sub_params["more"] = await links[1].get_attribute('href')
            sub_params["img"] = await img.get_attribute('src')
            index += 1
            params[index] = sub_params
        except:
            continue
    with open(os.path.abspath(f'client/src/assets/files/products.json'),'w') as file:
        file.write(json.dumps(params, indent=4, ensure_ascii=False))
                