import scrapy
from bato_scraper.bato_scraper.items import TheodoTeamItem

class TheodoSpider(scrapy.Spider):
    name = "theodo"

    def parse(self, response):
            item = TheodoTeamItem()
            item["name"] = response.xpath("//div[@class='quote']").get()
            item.save()
            yield item