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
       
       #Jobstreet Job Card
        articles = await page.locator('article').all()
        
        #Visible Job data Extraction
        for article in articles:      
            title = await article.locator('a[data-testid="job-card-title"]').text_content()
            company = await article.locator('a[data-type="company"]').text_content()
            job_link = await article.locator('a').first.get_attribute('href')
            apply_link = await article.get_attribute('data-job-id')

            locations = await article.locator('a[data-type="location"]').all()
            city = await locations[0].text_content() if locations else "N/A"
            region = await locations[1].text_content() if len(locations) > 1 else "N/A"
            
            base_url = "https://ph.jobstreet.com"
            yield {"Job Title": title.strip(),
                   "Company": company.strip(),
                   "City": city.strip(),
                   "Region": region.strip(),
                   "Job Link": base_url+job_link.strip(),
                   "Apply Link": base_url+"/job/"+apply_link+"/apply".strip()}
        
        
              
        await page.close()
