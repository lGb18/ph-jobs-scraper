import scrapy
from scrapy_playwright.page import PageMethod

class WebThreeSpider(scrapy.Spider):
    name = "web_three"
    start_urls = ["https://www.onlinejobs.ph/jobseekers/jobsearch"]
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 1,
        }
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta= {
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("wati_for_load_state", "networkidle"),
                    ],
                },
                callback=self.parse,
            
            )
    
    def parse(self, response):
        page = response.meta["playwright_page"]
        
        for jobcard in response.css('dt[class="col"]'):
            title = jobcard.css('h4::text').get()

            yield {
                "Job Title": title.strip() if title else None
            }




    