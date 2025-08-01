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
        # title = response.css('article::attr(aria-label)')
        # title = await page.locator('[data-testid="job-card-title"]').all()
        await page.wait_for_selector('article[aria-label]')  # Wait for JS content
        
        # Get aria-labels from all jobcard articles
        articles = await page.locator('article[aria-label]').all()
        for article in articles:
            title = await article.get_attribute('aria-label')
            
            yield {"title": title.strip()}
        
        # for titles in title_two:
        #     titles = await title_two.getall()   
        # for i, j in zip(articles, title_two):
        #     title = await i.get_attribute("aria-label")
        #     titles = await j.text_content("a")
                 
            
        # hyper_link = page.locator('[data-testid="job-list-item-link-overlay"]').get("href").all()
        # companies = page.locator('[data-type="company"]').get_by_role("link").all_text_contents()
        # titles = response.css(await page.locator('[data-testid="job-card-title"]')).all_text_contents()
        # titles = title.text_content()
        # for i, j,k in zip(title, hyper_link, companies):
        #     yield{
        #         "job_title" : i.strip(),
        #         "job_link" : j.get_attribute("href"),
        #         "company" : k.strip()
        #     }    
            # my_list.append({
            #     "title": job_title,
            #     "hyperlink": job_link,
            #     "company": company,
            # })
            # # yield {
            #     "title": job_title,
            #     "hyperlink": job_link,
            #     "company": company,
            # }
        # return my_list
        await page.close()

        # yield{
        #     "title": title.strip(),
        # }
        