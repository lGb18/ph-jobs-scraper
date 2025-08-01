import scrapy
from scrapy_playwright.page import PageMethod

class WebOne(scrapy.Spider):
    name = "web_one"
    start_urls = ["https://ph.jobstreet.com/"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("fill", "#keywords-input", "developer"),
                        PageMethod("click", "#searchButton"),
                    ],
            
                },
                callback=self.parse,
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
       
        await page.wait_for_selector('article[aria-label]') 
        
        articles = await page.locator('article[aria-label]').all()
        for article in articles:
            title = await article.get_attribute('aria-label')
            
            yield {"title": title.strip()}
        
        
        await page.close()
