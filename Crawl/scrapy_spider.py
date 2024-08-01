import scrapy
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from .models import ScrapedData
import logging
import w3lib.html


import scrapy
from scrapy.http import Request
import w3lib.html
from Crawl.models import ScrapedData

class MySpider(scrapy.Spider):
    name = "myspider"

    def __init__(self, url=None, keys=None, xpaths=None, user=None, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.keys = keys
        self.xpaths = xpaths
        self.user = user

    def parse(self, response):
        data = {}
        for key, xpath in zip(self.keys, self.xpaths):
            try:
                data[key] = w3lib.html.remove_tags(response.xpath(xpath).get(default='').strip()).replace('\\n', '')
            except ValueError as e:
                self.logger.error(f"Invalid XPath expression: {xpath} for key: {key}")
                data[key] = None

        # Save data to the database
        scraped_data = ScrapedData(data=data)
        scraped_data.user = self.user
        scraped_data.save()

def _run_spider(url, keys, xpaths, user):
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'ERROR',
    })
    process.crawl(MySpider, url=url, keys=keys, xpaths=xpaths, user=user)
    process.start()

def run_scrapy_spider(url, keys, xpaths, user):
    process = Process(target=_run_spider, args=(url, keys, xpaths, user))
    process.start()
    process.join()
