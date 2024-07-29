import scrapy
from scrapy.crawler import CrawlerProcess
from multiprocessing import Process
from .models import ScrapedData
import logging
import w3lib.html


class DynamicSpider(scrapy.Spider):
    name = 'dynamic_spider'

    def __init__(self, url, keys, xpaths, *args, **kwargs):
        super(DynamicSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.keys = keys
        self.xpaths = xpaths

    def parse(self, response):
        data = {}
        for key, xpath in zip(self.keys, self.xpaths):
            data[key] = w3lib.html.remove_tags(response.xpath(xpath).get(default='').strip())
        ScrapedData.objects.create(data=data)

def _run_spider(url, keys, xpaths):
    process = CrawlerProcess(settings={
        'LOG_LEVEL': 'ERROR',
    })
    process.crawl(DynamicSpider, url=url, keys=keys, xpaths=xpaths)
    process.start()

def run_scrapy_spider(url, keys, xpaths):
    process = Process(target=_run_spider, args=(url, keys, xpaths))
    process.start()
    process.join()
