from django.contrib import admin
from django.urls import path, include
from Crawl.views import ScraperAPIView, ScrapedDataListAPIView, download_csv, download_json, home, SignUpView, LoginView, LogoutView, profile_view, data_detail_view, change_password_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('api/signup/', SignUpView.as_view(), name='signup'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('profile/', profile_view, name='profile'),
    path('change-password/', change_password_view.as_view(), name= 'change-password'),
    path('api/scraper/', ScraperAPIView.as_view(), name='scraper-api'),
    path('api/scraped-data/', ScrapedDataListAPIView.as_view(), name='get-scraped-data'),
    path('api/detail/<int:data_id>', data_detail_view, name='data-detail'),
    path('download-csv/', download_csv, name='download-csv'),  
    path('download-json', download_json, name='download-json'),
]