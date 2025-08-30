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
            await bttn.get_by_text('Search', exact=True).click()
            

            for i in range(10):
                j_title = await page.locator('h3 [class="index_pc_jobHireTopTitle__zVsw_"]').all()
                # j_salary = await page.locator('span[class="index_pc_salaryText__k3HPE"]').all()
                for i in zip(j_title):
                    title = await i.text_content()
                    # salary = await j.text_content()

                    yield {
                        "Job Title": title.strip() if title else None,
                       
                    }
            
            
            await browser.close()
