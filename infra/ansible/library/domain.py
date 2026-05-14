from ansible.module_utils.basic import AnsibleModule
from faker import Faker
from playwright.async_api import async_playwright, TimeoutError, Page
from playwright_stealth import Stealth
from pydantic import BaseModel, field_validator
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from shutil import which
import asyncio
import base64
import requests
headless=False

response = requests.get("https://randomuser.me/api/?nat=us")
data = response.json()

phone = data['results'][0]['phone']
location = data['results'][0]['location']

crutch_path = "/home/yahal/Repos/Leams"


def download_base64_image(data_uri, output_filename="downloaded_image"):
    """
    Decodes a base64 Data URI and saves it as an image file.
    
    :param data_uri: The full base64 string starting with 'data:image/...'
    :param output_filename: The name of the file to save (without extension)
    :return: The filepath of the saved image
    """
    try:
        header, encoded_data = data_uri.split(',', 1)
        mime_type = header.split(';')[0]
        image_type = mime_type.split('/')[1]
        if image_type == "jpeg":
            image_type = "jpg"
        image_bytes = base64.b64decode(encoded_data)
        full_filepath = f"/home/yahal/Repos/Leams/infra/ansible/library/{output_filename}.{image_type}"
        with open(full_filepath, "wb") as file:
            file.write(image_bytes)
            
        print(f"Successfully saved image as: {full_filepath}")
        return full_filepath
        
    except ValueError:
        print("Error: Invalid data URI format. Ensure it starts with 'data:image/...'")
    except Exception as e:
        print(f"An error occurred: {e}")

class Sld(BaseModel):
    domain: str 
    @field_validator('domain')
    @classmethod
    def validate_mail_provider(cls, value: str) -> str:
        if value not in list(links.keys()):
            raise ValueError(f"Domen must be in list {list(links.keys())}")
        return value

links = {
    "gmail": "https://workspace.google.com/intl/en-US/gmail/",
    "proton": "https://account.proton.me/mail",
    "mailru": "https://mail.ru/"
}
class RegistrationError(Exception):
    pass

class LoginError(Exception):
    pass

async def ansible_module():
    module = AnsibleModule(
        argument_spec=dict(domain=dict(type='str', required=True))
    )
    domain = module.params['domain']
    email = module.params['email']
    password = module.params['password']
    provider = module.params['provider']
    await domain_site(domain, email, password)

# WARN: I strongly do not recommend to buy regional domains like because of the sharing the 
# personal info including passport's and following the laws of the region that you've chosen

async def domain_site(
    domain: str,
    email: str,
    password: None | str=None,
) -> None:
    software_names = [SoftwareName.CHROME.value]
    operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]   
    user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)
    user_agent = user_agent_rotator.get_random_user_agent()
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(executable_path=which("chromium"), headless=headless)
        context = await browser.new_context(user_agent=user_agent)
        page = await context.new_page()
        try:
            await page.goto(url="https://www.reg.ru",wait_until="domcontentloaded")
            await page.wait_for_selector(".h-button.profile-menu-login-button.qa-auth-btn")
            await page.click(".h-button.profile-menu-login-button.qa-auth-btn")
            if password is None:
                await reg(page=page, email=email)
                try:
                    await page.wait_for_selector("div[class='auth-form__message auth-form__message_info']", state="visible", timeout=10000)
                except TimeoutError:
                    print("Registration successful")
                else:
                    loop = asyncio.get_event_loop()
                    password = await asyncio.wait_for(loop.run_in_executor(None, input,"This email is taken but you haven't written the password.\nEnter the password: "), timeout=30) 
                    if password is not None:
                        while True: 
                            await login(page=page, email=email, password=password)
            else:
                await login(page, email, password)
            await page.goto(f"https://www.reg.ru/buy/domains/?place_of_order=cp_market&query={domain}",timeout=60000)
            await page.wait_for_selector("div[class='shadow-mode search-result-list']")
            elements = await page.locator("div[class='shadow-mode search-result-list']").all()
            if len(elements) == 0: 
                print("Something wrong")
                await asyncio.sleep(100)
            await elements[0].click()
            await asyncio.sleep(10)
            button_buy = page.locator("button[class='ds-button ds-button_size_xs ds-button_theme_secondary ds-button_icon_left ds-button_icon-only l-margin_left-large qa-cart-button']")
            await button_buy.first.wait_for(state="visible")
            await button_buy.first.click()
            print("Domain's chosen")
            await page.wait_for_selector("div[class='right-bar order-summary__desktop']")
            orders = page.locator("div[class='right-bar order-summary__desktop']")
            await page.wait_for_selector("span[class='icon icon_new-cross item__icon']")
            delete_buts = await orders.locator("span[class='icon icon_new-cross item__icon']").all()
            if len(delete_buts) >= 2:
                for but in delete_buts[1:]:
                    await but.click()
            await orders.locator("button[class='ds-button ds-button_size_s ds-button_theme_primary ds-button_icon_right ds-button_block right-bar-search-checkout__button']").click()
            await page.wait_for_selector("div[class='ds-drawer__wrapper ds-drawer__wrapper_mode_fullscreen ds-drawer__wrapper_mode_wide']")
            await page.keyboard.press("Escape")
            orders = page.locator("div[class='right-bar order-summary__desktop']")
            delete_buts = orders.locator("span[class='icon icon_new-cross item__icon']")
            await asyncio.sleep(2)
            try:
                await page.wait_for_selector("div[class='additional-domain-item additional-domain-item_banner domain-period-recommendation']")
                await page.click(
                    selector="div[class='additional-domain-item additional-domain-item_banner domain-period-recommendation'] input[class='ds-controls__input ds-switch__input']"
                )
            except TimeoutError:
                pass
            while await orders.locator("span[class='icon icon_new-cross item__icon']").count() >= 2:
                await orders.locator("span[class='icon icon_new-cross item__icon']").last.click()
                await asyncio.sleep(2)
            await asyncio.sleep(5)
            await orders.locator("button[class='ds-button ds-button_size_s ds-button_theme_primary ds-button_block']").click()
            await page.wait_for_selector("div[class='profiles']", state="visible")
            form_buy = page.locator("div[class='profiles']")
            input_form = form_buy.locator("input[class='ds-textfield ds-input ds-textfield_size_m ds-textfield_state_defaul']")
            await input_form.first.wait_for(state="visible")
            input_form = await input_form.all()
            fake = Faker("en_US")
            addr = [ 
                phone,
                fake.last_name(),
                fake.first_name(),
                f"0{location["postcode"]}",
                location["state"],
                location["city"], 
                f"{location['street']['name']} {location['street']['number']}" 
            ]
            for num, i in enumerate(input_form[1:len(addr)+1]):
                await i.fill(f"{addr[num]}")
            await form_buy.locator("button[class='ds-button ds-button_size_s ds-button_theme_primary qa_profile_save buttons-mobile__item profile-editor__button']").click()
            await page.wait_for_selector("div[class='pay-item-bar pay-item-bar_additional-actions qa-paytype-item-sbp qa-paytype-item-gate-paymaster']")
            await page.click("div[class='pay-item-bar pay-item-bar_additional-actions qa-paytype-item-sbp qa-paytype-item-gate-paymaster']")
            await page.wait_for_selector(".pm-toggle-container")
            rer = await page.locator(".pm-toggle-container").first.inner_text()
            print("Domain will cost: ", rer.replace('\n', ''))
            await page.wait_for_selector("img[class='pm-qr-code-payload']")
            qr_codes = await page.locator("img[class='pm-qr-code-payload']").all()
            nvnv = await qr_codes[0].get_attribute("src")
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
                        print("QR content:", qr_text)
                        qr = qrcode.QRCode()
                        qr.add_data(qr_text)
                        qr.make()
                        qr.print_ascii()
                    else:
                        print("No QR code found!")
            await browser.close()
        except:
            await page.screenshot(path="screenshot.png")

async def reg(page: Page, email: str):
    await page.click(".ds-segment-control__option.ds-segment-control__option_size_s.wrapper-sc__option")
    await page.wait_for_selector(".auth-form__content")
    await page.fill(
            selector=".qa-registr-form-field-email.ds-textfield.ds-input.ds-textfield_size_m.ds-textfield_state_default.qa-registr-form-field-email",
            value=email
    )
    await page.click(".ds-button.ds-button_size_s.ds-button_theme_primary.ds-button_block.auth-form__submit-button.qa-registr-form-register-btn")
    await page.wait_for_selector("div[class='smart-captcha'][data-testid='smartCaptcha-container'][style='height: 102px;']",state="visible")
    await page.click("div[class='smart-captcha'][data-testid='smartCaptcha-container'][style='height: 102px;']")

async def login(page: Page, email: str, password: str) -> None:
    try:
        await page.click(".ds-segment-control__option.ds-segment-control__option_style_selected.ds-segment-control__option_size_s.wrapper-sc__option")
        await page.fill(
                selector=".qa-auth-form-field-login.ds-textfield.ds-input.ds-textfield_size_m.ds-textfield_state_default.qa-auth-form-field-login",
                value=email
        )
        await page.fill(
                selector=".auth-form__password.qa-auth-form-field-pass.ds-textfield.ds-input.ds-textfield_size_m.ds-textfield_state_default.auth-form__password.qa-auth-form-field-pass",
                value=password
        )
        await page.click(".ds-button.ds-button_size_s.ds-button_theme_primary.ds-button_block.auth-form__submit-button.qa-auth-form-login-btn")
        await page.wait_for_selector(".auth-form__message.auth-form__message_error", state="visible")
    except LoginError:
        print("Invalid email or password")
        
if __name__ == "__main__":
    asyncio.run(domain_site(
        domain="leamsy.com",
        email="fsacsarydeaasssd@gmail.com",
    ))
