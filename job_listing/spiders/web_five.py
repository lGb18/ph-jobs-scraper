import scrapy
from scrapy_playwright.page import PageMethod


class WebFive(scrapy.Spider):
    name = "web_five"
    start_url = ["https://bossjob.ph"]


    def start_requests(self):
        for url in self.start_url:
            yield scrapy.Request(
                url,
                meta= {
                    "playwright" : True,
                    "playwright_include_page": True,
                    "playwright_page_methods": [
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("fill",'#rsc_select_1', "developer" ),
                        PageMethod("click", ".style_searchButton__FmHXW.yolo-search-button"),
                        # await page.locator('#rc_select_1').fill('developer');
                        # await page.getByRole('search').getByText('Search').click();
                    ],
                },
                callback=self.parse,
                
            )
    
    def parse(self, response):
        page = response.meta["playwright-page"]

