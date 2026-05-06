from ansible.module_utils.basic import AnsibleModule
from faker import Faker
from playwright.async_api import async_playwright, TimeoutError, BrowserContext
from playwright_stealth import Stealth
from pydantic import BaseModel, field_validator
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from shutil import which, rmtree, rmtree
import asyncio
import string
import secrets
import yaml
import base64
import os
import requests

async def ansible_module():
    module = AnsibleModule(
        argument_spec=dict(domain=dict(type='str', required=True))
    )
    domain = module.params['domain']
    email = module.params['email']
    password = module.params['password']
    provider = module.params['provider']
    await vps_site(domain, email, password)

def generate_google_password(length=16):
    letters = string.ascii_letters # a-z, A-Z
    digits = string.digits         # 0-9
    special_chars = "!@#$%^&*"     # Выбираем самые частые спецсимволы без кавычек
    alphabet = letters + digits + special_chars
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password) and 
            any(c.isupper() for c in password) and 
            any(c.isdigit() for c in password) and
            any(c in special_chars for c in password)):
            return password

async def vps_site(
    domain: str,
    email: str,
    password: None | str=None,
) -> None:
    rmtree("./user_data")
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./user_data", # Creates a folder in your project
            headless=False, # Google almost always blocks headless mode
            executable_path=which("chromium"),
            args=[
                # 1. Disable the "AutomationControlled" feature (Most Important)
                # This hides the navigator.webdriver flag
                "--disable-blink-features=AutomationControlled",
                # 2. Disable info bars (removes the "Chrome is being controlled by automated test software" banner)
                "--disable-infobars",
                # 3. Standardize window size (bots often use weird or tiny default sizes)
                "--start-maximized",
                # 4. Disable popup blocking (sometimes causes issues with automated flows)
                "--disable-popup-blocking",
                # 5. Disable default browser check
                "--no-default-browser-check",
                # 6. Disable plugins that might leak automation status
                "--disable-plugins-discovery",
                # 7. Prevent detection through background network requests/syncs
                "--disable-background-networking",
                "--disable-sync",
                # 8. Hide scrollbars (sometimes helps in headless, optional)
                "--hide-scrollbars",
                # 9. Sandbox flags (often required if running on Linux/Docker, helps prevent crashes that expose bots)
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage"
                
            ],
            ignore_default_args=["--enable-automation"] # <-- Вот эта строчка убирает плашку
        )
        page = await browser.new_page()
        await page.goto(url="https://senko.digital/",wait_until="domcontentloaded",timeout=60000)
        await page.locator("button[aria-label='Sign In']").click()
        await page.locator("button[aria-label='Register']").click()
        await page.locator("button[aria-label='Register']").click()
        inputs = await page.locator("form input").all()
        form = {
            "first_name" : "John",
            "last_name" : "Doe",
            "email" : email,
            "password" : generate_google_password(),
        }
        for num, inp in enumerate(inputs[:4]):
            await inp.fill(list(form.values())[num])
        await inputs[4].fill(list(form.values())[3])
        [await inp.click() for inp in await page.locator("input[type='checkbox']").all()]
        await page.locator("button:has-text('Create Account')").click()
        await mail_check(browser, email)
        await asyncio.sleep(300)

async def mail_check(
    context: BrowserContext,
    email: str,
    password: str = "25102006dfyZ()"
) -> bool:
    page = await context.new_page()
    await page.goto(url="https://workspace.google.com/intl/en-US/gmail/",timeout=60000)
    await page.evaluate("""document.querySelector('a[aria-label="Sign into Gmail"]').removeAttribute('target')""")
    await page.click("a[aria-label='Sign into Gmail']")
    await page.locator("input[type='email'][name='identifier']").first.fill(email)
    await page.locator('button:has(span:text-is("Next"))').first.click()
    print(password)
    await page.locator("input[type='password'][name='Passwd']").hover()
    await page.locator("input[type='password'][name='Passwd']").click()
    await page.locator("input[type='password'][name='Passwd']").first.fill(password)
    await page.locator('button:has(span:text-is("Next"))').first.hover()
    await page.locator('button:has(span:text-is("Next"))').first.click()
    await page.locator("input[type='password'][name='Passwd']").hover()
    await page.locator("input[type='password'][name='Passwd']").click()
    await page.locator("input[type='password'][name='Passwd']").first.fill(password)
    await page.locator('button:has(span:text-is("Next"))').first.hover()
    await page.locator('button:has(span:text-is("Next"))').first.click()
    await page.wait_for_selector("main samp, main input[type='tel']")
    if await page.locator("main input[type='tel']").count():
        await page.locator('input[id="phoneNumberId"][type="tel"]').fill("+79218780528")
        await page.locator('button:has(span:text-is("Send"))').first.click()
        loop = asyncio.get_event_loop()
        msg = await asyncio.wait_for(loop.run_in_executor(None, input,"Enter the password: "), timeout=60) 
        await page.locator('input[aria-label="Enter the code"][type="tel"]').fill(msg)
        await page.locator('button:has(span:text-is("Next"))').first.click()
        await page.locator('span:text-is("Continue")').first.click()
    elif await page.locator("main samp").count():
        await page.locator('span:text-is("Continue")').first.click(timeout=300000)
        pass
    # match way:
    #     case await way.locator("input[id='phoneNumberId'][type='tel']").count() > 0:
    #         await page.locator('input[id="phoneNumberId"][type="tel"]').fill("+79218780528")
    #         await page.locator('button:has(span:text-is("Send"))').first.click()
    #         loop = asyncio.get_event_loop()
    #         msg = await asyncio.wait_for(loop.run_in_executor(None, input,"Enter the password: "), timeout=60) 
    #         await page.locator('input[aria-label="Enter the code"][type="tel"]').fill(msg)
    #         await page.locator('button:has(span:text-is("Next"))').first.click()
    #         await page.locator('span:text-is("Continue")').first.click()
    #     case way.locator("samp"):
    #         pass
    return True


if __name__ == "__main__":
    asyncio.run(vps_site(
        domain="leamsy.com",
        email="juhacherenkov@gmail.com",
    ))

