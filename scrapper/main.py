import asyncio, time
from selenium_driverless import webdriver
from selenium_driverless.types.options import Options
import categories
from constants import COMPLETED, PROXY

async def main():
    options = Options()
    options.add_argument("--start-maximized")
    options.headless = True
    options.single_proxy = PROXY
    options.binary_location = "/home/juchi/.nix-profile/bin/chromium"
    async with webdriver.Chrome(options=options) as driver:
        await driver.get('https://www.twitch.tv', wait_load=True,timeout=90)
        ready_state = ''
        while ready_state != COMPLETED:
            ready_state = await driver.execute_script("return document.readyState")
            time.sleep(1)
        await categories.allCategories(driver)
asyncio.run(main())
