from django.contrib import admin
from django.urls import path, include
from Crawl.views import ScraperAPIView, ScrapedDataListAPIView, download_csv, home, SignUpView, LoginView, LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/scraper/', ScraperAPIView.as_view(), name='scraper-api'),
    path('api/scraped-data/', ScrapedDataListAPIView.as_view(), name='get-scraped-data'),
    path('download/', download_csv, name='download-csv'),   
]