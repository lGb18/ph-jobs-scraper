import scrapy
from scrapy_playwright.page import PageMethod, sync_playwright_page

class WebOne(scrapy.Spider):
    name = "web_one"
    start_urls = ["https://ph.jobstreet.com/"]

    def start_requests(self):
         
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_selector", "button:has-text('Submit search')"),
                        PageMethod("click", "button:has-text('Submit search')"),
                        PageMethod("wait_for_selector", "article[data-automation='job-card']", timeout=10000),
                    ],
                    "playwright_include_page": True,
                },
                callback=self.parse,
            )

    async def parse(self, response):
        page_count = 0
        for count in range(1,10):
            page_count += 1
           
        page = response.meta["playwright_page"]
        yield {
            "url": response.url,
            "title": await page.locator('xpath=//*[@id="jobcard-1"]').get_text_content(),
        }

    
        
        await page.close()