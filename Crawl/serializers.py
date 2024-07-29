from rest_framework import serializers
from .models import ScrapedData

class ScraperSerializer(serializers.Serializer):
    url = serializers.URLField()
    keys = serializers.ListField(
        child=serializers.CharField(max_length=100)
    )
    xpaths = serializers.ListField(
        child=serializers.CharField(max_length=500)
    )


class DataSerializer(serializers.ModelSerializer):
    class Meta:
        model = ScrapedData
        fields = '__all__'

