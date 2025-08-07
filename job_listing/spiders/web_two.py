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
                        PageMethod("click", 'input[type="submit"][value="Search"]'),
                        
                        
                    ]
                },
                callback=self.parse,
            )

    def parse(self, response):
        page = response.meta["playwright_page"]
        base_url = "https://philjobnet.gov.ph/job-vacancies"
        # await page.locator('input [id="ctl00_BodyContentPlaceHolder_Button1"]').click()

        for jobCard in response.css("div.jobcard"):
            title = jobCard.css('h1.jobtitle::text').get()

            yield {
                "JO": title.strip()

            }
            
        
             
