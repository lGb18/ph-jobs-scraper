import scrapy
from scrapy_playwright.page import PageMethod
import json
class WebFour(scrapy.Spider):
    name = "web_four"
    start_urls = ["https://www.kalibrr.com/_next/data/-fHXcxPVjzAEIkO7CkhrK/en/home/te/developer.json?param=te&param=developer"]
    custom_settings = {
        'CLOSESPIDER_PAGECOUNT': 5,
        }
    
    
    def parse(self, response):
        web_data = json.loads(response.body)

        job_list = [{ "Job Title": jobs["name"], "Company": jobs["companyName"] } for jobs in web_data['pageProps']['jobs']]
        yield from job_list