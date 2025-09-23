# Job Listing Scraper

Crawlers for job seeking in the Philippines.

## Features
- Input a keyword then wait.
- Output a json file of the listings.

## Tech
- [Scrapy](https://www.scrapy.org/docs) + [Playwright](https://playwright.dev/python/)

## Prerequisites
* Python 3.10+
  Download from [python.org](python.org)
  
## Installation
Clone the repository
```
git clone https://github.com/lGb18/ph-jobs-scraper
cd ph-jobs-scraper
```
Create a virtual environment and activate
```
python -m venv venv
source/venv/bin/activate
```
Install dependencies
```
pip install -r requirements.txt
```

## Run
Choose a spider and run using scrapy crawl

Example:
```
scrapy crawl -webOne
```
