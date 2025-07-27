from selenium_driverless.types.by import By
import asyncio, json, os

async def companies(driver):
    companies = await driver.find_elements(By.XPATH, '//a[@class="brand-card brand-card__link swiper-slide base-ui-slider__custom-slide-size_zDe base-ui-slider__slide-item_a4N"]')
    params = dict()
    index = 0
    for company in companies:
        try:
            img = await company.find_element(By.TAG_NAME, 'img')
            sub_params = dict()
            sub_params["img"] = await img.get_attribute('src')
            sub_params["link"] = await company.get_attribute('href')
            index += 1
            params[index] = sub_params
        except:
            continue
    with open(os.path.abspath(f'client/src/assets/files/companies.json'),'w') as file:
        file.write(json.dumps(params, indent=4, ensure_ascii=False))
                