import scrapy
# from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright

class WebTwo(scrapy.Spider):
    name = "web_two"
    start_urls = ["https://philjobnet.gov.ph/job-vacancies/"]

    async def parse(self, response):
        async with async_playwright() as p:
        
            browser = await p.chromium.launch(headless=False, devtools=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(response.url)
            page_num = 1
            for i in range(10):
                next_page = page_num + 1
                nexts_page = page.locator('#ctl00_BodyContentPlaceHolder_GridView1')
                # next_page.click()
                next_pagge = nexts_page.get_by_role('link', name=f'{str(next_page)}', exact=True)
                await next_pagge.click()

                page_num +=1
                j_title = await page.locator('h1').all()
                for jobCard in j_title:
                    title = await jobCard.text_content()

                    yield {
                        "JO": title.strip()

                    }

        
