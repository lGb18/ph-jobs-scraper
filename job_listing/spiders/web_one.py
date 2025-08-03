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
                        PageMethod("wait_for_selector", '[data-testid="job-card-title"]', timeout=15000),
                    ],
            
                },
                callback=self.parse,
        )

    async def parse(self, response):
        page = response.meta["playwright_page"]
       
        articles = await page.locator('article').all()
        
        for article in articles:
            
            title = await article.locator('a[data-testid="job-card-title"]').text_content()
            company = await article.locator('a[data-type="company"]').text_content()
            
            locations = await article.locator('a[data-type="location"]').all()
            city = await locations[0].text_content() if locations else "N/A"
            region = await locations[1].text_content() if len(locations) > 1 else "N/A"
            yield {"Job Title": title.strip(),
                   "Company": company.strip(),
                   "City": city.strip(),
                   "Region": region.strip()}
        
              
        await page.close()
