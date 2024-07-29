# mycrawler/spiders/crawlspider.py

import scrapy

class CrawlspiderSpider(scrapy.Spider):
    name = "crawlspider"
    custom_settings = {
        'ITEM_PIPELINES': {
            '__main__.CollectItemsPipeline': 100,
        }
    }

    def __init__(self, url=None, xpaths=None, *args, **kwargs):
        super(CrawlspiderSpider, self).__init__(*args, **kwargs)
        self.start_urls = [url]
        self.xpaths = xpaths
        self.items = []

    def parse(self, response):
        result = {}
        for key, xpath in self.xpaths.items():
            result[key] = response.xpath(xpath).get()
        self.items.append(result)
        yield result

class CollectItemsPipeline:
    def process_item(self, item, spider):
        spider.items.append(item)
        return item
