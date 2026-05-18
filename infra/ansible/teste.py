from playwright.sync_api import sync_playwright
import time

def test_gui():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,
        )
        page = browser.new_page()
        page.goto("https://bhandarisanjeeev.com.np/")
        page.pause()
        time.sleep(5)
        browser.close()

if __name__ == "__main__":
    test_gui()
