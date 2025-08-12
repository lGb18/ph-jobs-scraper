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
            base_url = "https://philjobnet.gov.ph"
            
            # Search wtih Keyword
            await page.locator('#ctl00_BodyContentPlaceHolder_searchterm').click()
            await page.locator('#ctl00_BodyContentPlaceHolder_searchterm').fill('developer')
            # button_click = page.locator('#ctl00_BodyContentPlaceHolder_Button1')
            await page.get_by_role('button', name= "Search" ).click()
            
            
            for i in range(3):
                # Selector reference
                j_title = await page.locator('h1').all()
                j_card = await page.locator('td a[class="nolink"]').all()
                j_company = await page.locator('span.companytitle').all()
                j_location = await page.locator('div.col-lg-5.col-sm-12').all()
                # Extract loop
                for i, j, k, l in zip(j_title,j_card, j_company, j_location):
                    title = await i.text_content()
                    link = await j.get_attribute('href')
                    company = await k.text_content()
                    location = await l.text_content()
                    yield {
                        "JO": title.strip() if title else None,
                        "Job Link": base_url + link.strip() if link else None,
                        "Company": company.strip() if company else None,
                        "Location": location.strip() if location else None

                    }
                # Next Page Reference
                next_page = page_num + 1
                nexts_page = page.locator('#ctl00_BodyContentPlaceHolder_GridView1')
                # Click Next Page
                next_pagge = nexts_page.get_by_role('link', name=f'{str(next_page)}', exact=True)
                await next_pagge.click()

                page_num +=1

               
                

        
