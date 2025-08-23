import scrapy
from scrapy_playwright.page import PageMethod
import json
class WebFour(scrapy.Spider):
    name = "web_four"
    start_urls = ["https://www.kalibrr.com/kjs/job_board/search?limit=500&offset=0&text=developer"]
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 5,
        }
    
    
    def parse(self, response):
        web_data = json.loads(response.body)

        job_list = [{ "Job Title": jobs["name"], "Company": jobs["company_name"], "Job Link": f'https://www.kalibrr.com/c/{jobs["company"]["code"]}/jobs/{jobs["id"]}/{jobs["slug"]}' } for jobs in web_data['jobs']]
        yield from job_list