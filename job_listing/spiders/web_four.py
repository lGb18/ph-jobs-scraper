import scrapy
from scrapy_playwright.page import PageMethod

class WebFour(scrapy.Spider):
    name = "web_four"
    start_urls = ["https://www.kalibrr.com/home/te/DEVELOPER"]
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 5,
        }
    
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("wait_for_load_state", "networkidle"),                           
                    ],
            
                },
                callback=self.parse,
        )

    def parse(self, response):
        page = response.meta["playwright_page"]

        for jobcards in ('h2.a'):
            title = response.css('::text').get()
            job_link = response.css('::attr(href)').get()

            yield {
                "Job Title": title.strip() if title else None,
                "Job Link": job_link.strip() if title else None
            }