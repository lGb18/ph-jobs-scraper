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
            await page.locator('#rc_select_1').press('Enter')
            await page.wait_for_selector('div [class="style_contentLeft__RHYay"]', state='visible', timeout=None)
            await page.wait_for_load_state(state='load', timeout=None)
            
            
            j_title = await page.locator('div [data-sentry-component="JobCardPc"] h3').all()
            j_salary = await page.locator('div [data-sentry-component="JobCardPc"] span.index_pc_salaryText__k3HPE').all()
            # j_salary = await page.locator('span[class="index_pc_salaryText__k3HPE"]').all()
            for i, j in zip(j_title, j_salary):
                title = await i.text_content()
                salary = await j.text_content()
                yield {
                        "Job Title": title.strip(),
                        "Salary": salary.strip()
                }
               

                    
            
            await page.pause()
           
