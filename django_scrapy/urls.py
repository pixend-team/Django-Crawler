from django.contrib import admin
from django.urls import path, include
from Crawl.views import ScraperAPIView, ScrapedDataListAPIView, download_csv

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/scraper/', ScraperAPIView.as_view(), name='scraper-api'),
    path('api/scraped-data/', ScrapedDataListAPIView.as_view(), name='get-scraped-data'),
    path('download/', download_csv, name='download-csv'),   
]