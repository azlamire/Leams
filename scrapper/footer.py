from selenium_driverless.types.by import By
import asyncio, json, os

async def footer(driver):
    footer = await driver.find_element(By.TAG_NAME,'footer')
    divs = await footer.find_elements(By.TAG_NAME, 'div')
    await driver.execute_script("""
        window.scrollTo(0,2000)
    """)
    script = """
        const style = window.getComputedStyle(argument[0])
        return style.backgroundImage
    """
    for div in divs:
        is_background_image = await driver.execute_script(script, div)
        if is_background_image:
            print(is_background_image)

