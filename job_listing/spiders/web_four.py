import scrapy
from scrapy_playwright.page import PageMethod

class WebFour(scrapy.Spider):
    name = "web_four"
    start_urls = ["https://www.kalibrr.com/_next/data/-fHXcxPVjzAEIkO7CkhrK/en/home/te/developer.json?param=te&param=developer"]
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

        print(response.body)
        # for jobcards in response.css('main'):
        #     title = jobcards.css('h2.a::text').get()
        #     job_link = jobcards.css('h2.a::attr(href)').get()

        #     yield {
        #         "Job Title": title.strip() if title else None,
        #         "Job Link": job_link.strip() if title else None
        #     }