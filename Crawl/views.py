from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ScraperSerializer, DataSerializer, UserSerializer
from .scrapy_spider import run_scrapy_spider
from .models import ScrapedData
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny
from .forms import SignUpForm, LoginForm, CrawlForm
from django.contrib import messages

class SignUpView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'User created successfully')
            return redirect('login')
        return render(request, 'signup.html', {'form': form})

class LoginView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print(user)
                login(request, user)
                messages.success(request, 'Logged in successfully')
                return redirect('home')
            messages.error(request, 'Invalid credentials')
        return render(request, 'login.html', {'form': form})

class LogoutView(APIView):
    @method_decorator(login_required)
    def get(self, request):
        logout(request)
        messages.success(request, 'Logged out successfully')
        return redirect('login')

class ScraperAPIView(APIView):
    
    def get(self, request):
        form = CrawlForm()
        return render(request, 'scraper.html', {'form': form})
    
    def post(self, request, *args, **kwargs):
        form = CrawlForm(data=request.POST)
        if form.is_valid():
            url = form.cleaned_data['url']
            keys = form.cleaned_data['keys']
            xpaths = form.cleaned_data['xpaths']
            user = request.user
            # Run the scrapy spider
            try:
                run_scrapy_spider(url, keys, xpaths, user)
                messages.success(request, 'Scraping started successfully')
                return redirect('scraper-api')
            except Exception as e:
                messages.error(request, f'An error occurred: {str(e)}')
                return redirect('scraper-api')
        
        return render(request, 'scraper.html', {'form': form})


class ScrapedDataListAPIView(generics.ListAPIView):
    queryset = ScrapedData.objects.all()
    serializer_class = DataSerializer


def download_csv(request):
    user = request.user
    try:
        scraped_data_objects = ScrapedData.objects.filter(user=user)
    except TypeError or not user:
        return HttpResponse("Bad Request")
    data_list = [data.data for data in scraped_data_objects]
    df = pd.DataFrame(data_list)
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="scraped_data.csv"'
    df.to_csv(response, index=False)
    return response

def home(request):
    return render(request, 'home.html')
