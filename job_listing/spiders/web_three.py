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
        
        for jobcard in response.css('div[style="position: relative;"]'):
            title = jobcard.css('h4::text').get()
            posted_date = jobcard.css('em::text').get()
            post_author = jobcard.css('p::text').get()

            yield {
                "Job Title": title.strip() if title else None,
                "Date Posted": posted_date.strip() if posted_date else None,
                "Author": post_author.strip() if post_author else None
            }




    