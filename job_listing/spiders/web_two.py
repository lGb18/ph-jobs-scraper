import scrapy
from scrapy_playwright.page import PageMethod

class WebTwo(scrapy.Spider):
    name = "web_two"
    start_urls = ["https://philjobnet.gov.ph/job-vacancies/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [   
                        PageMethod("fill", "#ctl00_BodyContentPlaceHolder_searchterm", "developer"),
                        # PageMethod("click", 'input[type="submit"][value="Search"]'),
                        
                        
                    ]
                },
                callback=self.parse,
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        base_url = "https://philjobnet.gov.ph/job-vacancies"
        # await page.locator('input [id="ctl00_BodyContentPlaceHolder_Button1"]').click()

        for jobCard in response.css("div.jobcard"):
            title = jobCard.css('h1.jobtitle::text').get()

            yield {
                "JO": title.strip()

            }
        page_num = 1
        
        next_page = response.css('a::attr(href)')
        if await page.is_visible('a[href="javascript:__doPostBack(\'ctl00$BodyContentPlaceHolder$GridView1\',\'Page$Last\')"]'):
            page_num += 1
            await page.evaluate(f"window.__doPostBack('ctl00$BodyContentPlaceHolder$GridView1','Page$ + {page_num}')")
            current_url = response.url
            yield scrapy.Request(
               url=current_url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                       
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("wait_for_load_state", "networkidle"),
                    ]
                },
                callback=self.parse,
            )
        
