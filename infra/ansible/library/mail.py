import functools
from ansible.module_utils.basic import AnsibleModule
from playwright.async_api import async_playwright, Page
from playwright_stealth import Stealth
from shutil import which, rmtree
from faker import Faker
import traceback
import asyncio
import base64
import secrets
import string
import os 
from requests import get



def download_base64_image(data_uri, output_filename="downloaded_image"):
    """
    Decodes a base64 Data URI and saves it as an image file.
    """
    try:
        if data_uri.startswith("png;base64,") or data_uri.startswith("jpeg;base64,"):
            data_uri = "data:image/" + data_uri
            
        header, encoded_data = data_uri.split(',', 1)
        mime_type = header.split(';')[0]
        if '/' in mime_type:
            image_type = mime_type.split('/')[1]
        else:
            image_type = "png"
            
        if image_type == "jpeg":
            image_type = "jpg"
            
        encoded_data = "".join(encoded_data.split())
        missing_padding = len(encoded_data) % 4
        if missing_padding:
            encoded_data += '=' * (4 - missing_padding)
        image_bytes = base64.b64decode(encoded_data)
        full_filepath = f"/home/yahal/Repos/Leams/infra/ansible/library/{output_filename}.{image_type}"
        
        with open(full_filepath, "wb") as file:
            file.write(image_bytes)
            
        print(f"Successfully saved image as: {full_filepath}")
        return full_filepath
        
    except Exception as e:
        print(f"An error occurred: {e}")

response = get("https://randomuser.me/api/?nat=us")
data = response.json()

phone = data['results'][0]['phone']
location = data['results'][0]['location']

crutch_path = "/home/yahal/Repos/Leams"


class RegistrationError(Exception):
    pass

class LoginError(Exception):
    pass


# WARN: I strongly do not recommend to buy regional domains like because of the sharing the 
# personal info including passport's and following the laws of the region that you've chosen

def generate_google_password(length=16):
    letters = string.ascii_letters # a-z, A-Z
    digits = string.digits         # 0-9
    special_chars = "!@#$%^&*"
    alphabet = letters + digits + special_chars
    while True:
        password = ''.join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in password) and 
            any(c.isupper() for c in password) and 
            any(c.isdigit() for c in password) and
            any(c in special_chars for c in password)):
            return password

def start(func):
    @functools.wraps(func)
    async def wrapper(*args,email, headless=True, **kwargs):
        user_dir = "./user_data"
        async with Stealth().use_async(async_playwright()) as p:
            browser = await p.chromium.launch_persistent_context(
                user_data_dir="./user_data",
                headless=headless,
                executable_path=which("chromium"),
                args=[
                    # 1. Disable the "AutomationControlled" feature 
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
                ]
            )
            page = await browser.new_page()
            try:
                return await func(*args, email=email, page=page, **kwargs)
            finally:
                await browser.close()
                rmtree(user_dir)
    return wrapper

@start
async def google(
    email: str,
    page: Page
):
        await page.goto("https://workspace.google.com/intl/en-Us/gmail/", wait_until="domcontentloaded")
        await page.locator('span.button-label:has-text("Create an account")').first.click()
        await page.locator("a[data-g-action='for my personal use']").first.click()
        await page.locator("input[name='firstName']").fill("John")
        await page.locator("input[name='lastName']").fill("Doe")
        await page.locator('button:has(span:text-is("Next"))').first.click()
        await page.locator('input[type="tel"][id="day"]').first.fill("31")

        await page.locator('input[type="tel"][id="year"]').first.fill("2005")
        await page.locator('.VfPpkd-aPP78e').first.click()
        await page.locator("ul[aria-label='Month']").press("Enter")
        await page.locator('.VfPpkd-aPP78e').nth(1).click()
        await page.locator("ul[aria-label='Gender']").press("Enter")
        await page.locator('button:has(span:text-is("Next"))').first.click()
        await page.locator('input[aria-label="Username"]').first.fill(email)
        await page.locator('button:has(span:text-is("Next"))').first.click()
        password = generate_google_password()
        await page.locator('input[type="password"]').nth(0).fill(password)
        await page.locator('input[type="password"]').nth(1).fill(password)
        await page.locator('button:has(span:text-is("Next"))').first.click()
        nvnv = await page.locator('img[alt="Image of QR code to scan with the camera on your mobile device."]').get_attribute('src')
        if nvnv is not None:
            jffj = download_base64_image(nvnv)
            from PIL import Image
            from pyzbar.pyzbar import decode
            import qrcode
            if jffj is not None:
                img = Image.open(jffj)
                data = decode(img)
                if data:
                    qr_text = data[0].data.decode()
                    qr = qrcode.QRCode()
                    qr.add_data(qr_text)
                    qr.make()
                    qr.print_ascii()
                    os.remove(jffj)
                else:
                    print("No QR code found!")
        await asyncio.sleep(1000)
        return email,password

@start
async def outlook(
    email: str,
    page: Page
):
        await page.goto("https://www.microsoft.com/en-us/microsoft-365/outlook/email-and-calendar-software-microsoft-outlook/", wait_until="domcontentloaded")
        await page.locator("a:has-text('Sign in'):visible").nth(0).hover()
        await page.locator("a:has-text('Sign in'):visible").nth(0).click(timeout=60000)
        await page.locator("a[id='signup']").first.hover()
        await page.locator("a[id='signup']").first.click(timeout=60000)
        await page.locator("input[type='email']").hover()
        await page.locator("input[type='email']").click()
        await page.locator("input[type='email']").fill(email)
        await page.locator('button:has-text("Next")').first.hover()
        await page.locator('button:has-text("Next")').first.click()
        password = generate_google_password()
        await page.locator("input[type='password']").hover()
        await page.locator("input[type='password']").click()
        await page.locator("input[type='password']").fill(password)
        await page.locator('button:has-text("Next")').first.hover()
        await page.locator('button:has-text("Next")').first.click()
        await page.locator("button[aria-label='Birth month'][id='BirthMonthDropdown']").hover()
        await page.locator("button[aria-label='Birth month'][id='BirthMonthDropdown']").click()
        await page.keyboard.press("Enter")
        await page.locator("button[aria-label='Birth day'][id='BirthDayDropdown']").hover()
        await page.locator("button[aria-label='Birth day'][id='BirthDayDropdown']").click()
        await page.keyboard.press("Enter")
        await page.locator("input[name='BirthYear'][aria-label='Birth year']").hover()
        await page.locator("input[name='BirthYear'][aria-label='Birth year']").click()
        await page.locator("input[name='BirthYear'][aria-label='Birth year']").fill("2000")
        await page.locator('button:has-text("Next")').first.hover()
        await page.locator('button:has-text("Next")').first.click()
        fake = Faker("en_US")
        await asyncio.sleep(1)
        await page.locator("input[name='firstNameInput'][id='firstNameInput']").hover()
        await page.locator("input[name='firstNameInput'][id='firstNameInput']").click()
        await page.locator("input[name='firstNameInput'][id='firstNameInput']").fill(fake.first_name())
        await page.locator("input[name='lastNameInput'][id='lastNameInput']").hover()
        await page.locator("input[name='lastNameInput'][id='lastNameInput']").click()
        await page.locator("input[name='lastNameInput'][id='lastNameInput']").fill(fake.first_name())
        await page.locator('button:has-text("Next")').first.hover()
        await page.locator('button:has-text("Next")').first.click()
        return email,password


@start
async def proton(
    email: str,
    page: Page
):
        await page.goto("https://mail.proton.me/", wait_until="domcontentloaded")
        await page.locator("a:has-text('Create account')").hover()
        await page.locator("a:has-text('Create account')").click()
        await page.locator('div[id="free-price"]').first.hover()
        await page.locator('div[id="free-price"]').first.click()
        password = generate_google_password()
        await page.frame_locator('iframe[title="Email address"]').locator('input[id="username"]').nth(0).hover()
        await page.frame_locator('iframe[title="Email address"]').locator('input[id="username"]').nth(0).click()
        await page.frame_locator('iframe[title="Email address"]').locator('input[id="username"]').nth(0).fill(email)
        await page.locator('input[id="password"]').nth(0).hover()
        await page.locator('input[id="password"]').nth(0).click()
        await page.locator('input[id="password"]').nth(0).fill(password)
        await page.locator('input[id="password-confirm"]').nth(0).hover()
        await page.locator('input[id="password-confirm"]').nth(0).click()
        await page.locator('input[id="password-confirm"]').nth(0).fill(password)
        await page.locator('button:has-text("Start using Proton Mail now")').hover()
        await page.locator('button:has-text("Start using Proton Mail now")').click()
        await page.locator('button:has-text("No, thanks")').hover()
        await page.locator('button:has-text("No, thanks")').click()
        await page.pause()
        return email,password
        
async def tuta():
    pass

async def yandex():
    pass

async def mailru():
    pass



PROVIDERS_MAP = {
    "proton": proton,
    "tuta": tuta,
    "outlook": outlook,
    "google": google,
    "yandex": yandex,
    "mailru": mailru
}


async def ansible_module():
    module = AnsibleModule(
        argument_spec=dict(
            addr=dict(type='str', required=True),
            password=dict(type='str', required=True),
        )
    )    
    try: 
        addr = str(module.params['addr'])
        provider = addr[addr.find("@")+1:addr.find(".")]
        addr = addr[:addr.find("@")]
        handler = PROVIDERS_MAP.get(provider)
        if handler is None:
            raise ValueError(f"Провайдер {provider} не поддерживается!")
        headless=False
        account = await handler(email=addr, headless=headless)
        
        module.exit_json(changed=True, msg=f"Успешно обработан {account}")
    except Exception as e:
        module.fail_json(msg=f"Произошла ошибка: {str(e)}", traceback=traceback.format_exc())
if __name__ == "__main__":
    asyncio.run(ansible_module())
