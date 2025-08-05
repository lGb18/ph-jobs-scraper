import scrapy
from scrapy_playwright import PageMethod


class WebTwo(scrapy.Spider):
    name = "web_two"
    start_urls = ["https://onlinejobs.ph"]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(
                url,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [   
            
                    ]
                },
                callback=self.parse,
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        base_url = "https://onlinejobs.ph"
        
             
