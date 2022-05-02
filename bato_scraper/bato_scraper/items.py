# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy_djangoitem import DjangoItem
from bato_app.models import TheodoTeam

class TheodoTeamItem(DjangoItem):
    django_model = TheodoTeam