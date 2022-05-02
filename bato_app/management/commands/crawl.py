from django.core.management.base import BaseCommand
from bato_scraper.bato_scraper.spiders.bato_spider import TheodoSpider
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

class Command(BaseCommand):
    help = "Release the spiders"
    def add_arguments(self , parser):
        parser.add_argument('url' , nargs='+' , type=str, 
        help='add url')

    def handle(self, *args, **options):
        process = CrawlerProcess(get_project_settings())
        
        process.crawl(TheodoSpider,start_urls=options['url'])
        process.start()