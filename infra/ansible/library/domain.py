#!/usr/bin/env uv
from playwright.async_api import async_playwright
import asyncio

url = "https://www.reg.ru"
async def buy_domain():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url, wait_until="load")

asyncio.run(buy_domain())

