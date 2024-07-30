from rest_framework import serializers
from .models import ScrapedData
from django.contrib.auth.models import User

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

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user