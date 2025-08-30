import scrapy
from playwright.async_api import async_playwright


class WebFive(scrapy.Spider):
    name = "web_five"
    start_urls = ["https://bossjob.ph"]

    async def parse(self, response):
        async with async_playwright() as p:
        
            browser = await p.chromium.launch(headless=False, devtools=False)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(response.url)

            await page.locator('#rc_select_1').click()
            await page.locator('#rc_select_1').fill('developer')
            bttn = page.get_by_role('search')
            await bttn.get_by_text('Search').click()


