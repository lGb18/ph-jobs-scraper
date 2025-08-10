import scrapy
# from scrapy_playwright.page import PageMethod
from playwright.async_api import async_playwright

class WebTwo(scrapy.Spider):
    name = "web_two"
    start_urls = ["https://philjobnet.gov.ph/job-vacancies/"]

    # def start_requests(self):
    #     for url in self.start_urls:
    #         yield scrapy.Request(
    #             url,
    #             meta={
    #                 "playwright": True,
    #                 "playwright_include_page": True,
    #                 "playwright_page_methods": [   
    #                     PageMethod("fill", "#ctl00_BodyContentPlaceHolder_searchterm", "developer"),
    #                     # PageMethod("click", 'input[type="submit"][value="Search"]'),
                        
                        
    #                 ]
    #             },
    #             callback=self.parse,
    #         )

    async def parse(self, response):
        async with async_playwright() as p:
        # Launch browser in non-headless mode with DevTools
            browser = await p.chromium.launch(headless=False, devtools=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto(response.url)
        # base_url = "https://philjobnet.gov.ph/job-vacancies"
        # await page.locator('input [id="ctl00_BodyContentPlaceHolder_Button1"]').click()
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
        # page_num = 1
        
        # data_table = page.locator('#ctl00_BodyContentPlaceHolder_GridView1')
        

        # while True:
           
        #     next_page = data_table.get_by_role('link', name=f'{page_num + 1}', exact=True)
        #     await next_page.click()
        #     page_num += 1 
        #     page.wait_for_timeout(3000)
        #     yield scrapy.Request(
        #         url=page.url,
        #         meta={
        #             "playwright": True,
        #             "playwright_include_page": True,
        #             "playwright_page_methods": [
        #                 PageMethod("wait_for_selector", '#ctl00_BodyContentPlaceHolder_GridView1'),
        #                 PageMethod("wait_for_load_state", "networkidle"),
        #                 PageMethod("wait_for_load_state", "domcontentloaded"),

        #             ],
        #         },
        #         callback=self.parse,
        #     )
        
