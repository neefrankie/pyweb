
import asyncio
import random
from playwright.async_api import async_playwright
from playwright_stealth import stealth_async

from dotenv import dotenv_values

env = dotenv_values(".env")

VISA_EMAIL = env["US_VISA_EMAIL"]
VISA_PASS = env["US_VISA_PASS"]

async def main():
    js = """
Object.defineProperty(navigator, 'webdriver', {get: () => undefined })
"""
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False, slow_mo=50, timeout=0)
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        )
        page = await context.new_page()
        await page.add_init_script(js)
        await page.set_extra_http_headers({
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
        })
        # await stealth_async(page)

        await page.goto("https://portal.ustraveldocs.com/?country=China&language=Simplified%20Chinese")
        # await asyncio.sleep(random.randint(1, 5))
        await page.wait_for_timeout(10000)
        
        await page.mouse.move(100, 100)
        await page.wait_for_timeout(2000)
        await page.mouse.click(200, 200)
        
        # await page.get_by_role("checkbox").check(timeout=300000)
        
        await asyncio.sleep(30)
        
        await page.get_by_label("Email").fill(VISA_EMAIL)
        await page.get_by_label("Password").fill(VISA_PASS)

        await asyncio.sleep(random.randint(1, 5))

        # await page.frame_locator("css.ctp-checkbox-label").get_by_role("input", checked=False).check()

        # await page.get_by_role("button", name="登录").click()
        await page.locator("css=#loginPage:SiteTemplate:siteLogin:loginComponent:loginForm:loginButton").click()

        await asyncio.sleep(60)
        await page.screenshot(path="tmp/screenshot.png", full_page=True)
        await browser.close()
        
        
asyncio.run(main())