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

            #Search Action
            await page.locator('#rc_select_1').click()
            await page.locator('#rc_select_1').fill('developer')
            await page.locator('#rc_select_1').press('Enter')

            #Wait for Load
            await page.wait_for_selector('div [class="style_contentLeft__RHYay"]', state='visible', timeout=None)
            await page.wait_for_load_state(state='load', timeout=None)
            
            #CSS References
            j_title = await page.locator('div [data-sentry-component="JobCardPc"] h3').all()
            j_salary = await page.locator('div [data-sentry-component="JobCardPc"] span.index_pc_salaryText__k3HPE').all()
            j_company = await page.locator('div [data-sentry-component="JobCardPc"] p').all()
            j_location = await page.locator('div [data-sentry-component="JobCardPc"] span.index_pc_jobCardLocationItem__Gzujh:nth-child(3)').all()
            
            for i, j, k, l in zip(j_title, j_salary, j_company, j_location):
                title = await i.text_content()
                salary = await j.text_content()
                company = await k.text_content()
                location = await l.text_content()
                yield {
                        "Job Title": title.strip(),
                        "Salary": salary.strip(),
                        "Company": company.strip(),
                        "Location": location.strip(),
                        "Link": response.url
                }
                
            await page.close()
           
