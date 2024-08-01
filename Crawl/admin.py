from django.contrib import admin
from .models import ScrapedData

# Register your models here.

@admin.register(ScrapedData)
class Crawl_resultAdmin(admin.ModelAdmin):
    '''Admin View for Crawl_result'''
    fields = ['data', 'user']

    list_display = ('pk',)