from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ScraperSerializer, DataSerializer
from .scrapy_spider import run_scrapy_spider
from .models import ScrapedData
from django.http import HttpResponse
import csv
import pandas as pd

class ScraperAPIView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = ScraperSerializer(data=request.data)
        if serializer.is_valid():
            url = serializer.validated_data['url']
            keys = serializer.validated_data['keys']
            xpaths = serializer.validated_data['xpaths']
            
            # Run the scrapy spider
            try:
                run_scrapy_spider(url, keys, xpaths)
                return Response({'message': 'Scraping started successfully'}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'message': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScrapedDataListAPIView(generics.ListAPIView):
    queryset = ScrapedData.objects.all()
    serializer_class = DataSerializer


def download_csv(request):
    scraped_data_objects = ScrapedData.objects.all()
    data_list = [data.data for data in scraped_data_objects]
    df = pd.DataFrame(data_list)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scraped_data.csv"'
    df.to_csv(response, index=False)
    return response

