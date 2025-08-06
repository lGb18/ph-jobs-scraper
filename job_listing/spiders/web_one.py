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
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("fill", "#keywords-input", "developer"),
                        PageMethod("click", "#searchButton"),
                        PageMethod("wait_for_selector", '[data-testid="job-card-title"]', timeout=15000),
                                              
                    ],
            
                },
                callback=self.parse,
        )
    
    def parse(self, response):
        base_url = "https://ph.jobstreet.com"

        #Extract
        for article in response.css("article"):
            title = article.css('a[data-testid="job-card-title"]::text').get()
            company = article.css('a[data-type="company"]::text').get()
            job_link = article.css('a::attr(href)').get()
            apply_link = article.attrib.get("data-job-id")

            locations = article.css('a[data-type="location"]::text').getall()
            city = locations[0] if len(locations) > 0 else "N/A"
            region = locations[1] if len(locations) > 1 else "N/A"
        #Jobstreet Job Card
            yield {
                "Job Title": title.strip() if title else None,
                "Company": company.strip() if company else None,
                "City": city.strip(),
                "Region": region.strip(),
                "Job Link": base_url + job_link.strip() if job_link else None,
                "Apply Link": base_url + "/job/" + apply_link + "/apply" if apply_link else None
            }
       
        
        next_page = response.css('a[rel="nofollow next"]::attr(href)').get()
        if next_page:
            yield scrapy.Request(
                url=base_url + next_page,
                meta={
                    "playwright": True,
                    "playwright_include_page": True,
                    "playwright_page_methods":[
                       
                        PageMethod("wait_for_load_state", "domcontentloaded"),
                        PageMethod("wait_for_load_state", "networkidle"),
                        PageMethod("wait_for_selector", '[data-testid="job-card-title"]', timeout=15000),
                    ],
                },
                callback=self.parse,
            )
        
            
           

           
        
