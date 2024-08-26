from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import View
from .serializers import ScraperSerializer, DataSerializer, UserSerializer, UserRegisterSerializer, ChangePasswordSerializer
from .scrapy_spider import run_scrapy_spider
from .models import ScrapedData
from django.http import HttpResponse
import pandas as pd
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from rest_framework.permissions import AllowAny, IsAuthenticated
from .forms import SignUpForm, LoginForm, CrawlForm, ChangePasswordForm
from django.contrib import messages


class SignUpView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        form = SignUpForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = SignUpForm(request.POST)
        if form.is_valid():
            serializer_class = UserRegisterSerializer(data=form.cleaned_data)
            if serializer_class.is_valid():
                serializer_class.save()
                messages.success(request, 'User created successfully')
                user = authenticate(request, username=form.cleaned_data.get('username'), password=form.cleaned_data.get('password'))
                login(request=request, user=user)
                # send_welcome_email(user_id=user.pk)
                return redirect('home')
            else:
                messages.error(request, serializer_class.errors)
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
            try:
                user = authenticate(request, username=username, password=password)
            except:
                messages.error(request, message="Invalid username or password")
            if user is not None:
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
            keys = form.cleaned_data['keys'].split(',')
            xpaths = form.cleaned_data['xpaths'].split(',')
            user = request.user
            # Run the scrapy spider
            try:
                run_scrapy_spider(url, keys, xpaths, user)
                messages.success(request, 'Scraped successfully')
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

@login_required
def profile_view(request):
    user = request.user
    scraped_data = ScrapedData.objects.filter(user=user).order_by('-created')
    
    if request.method == 'POST':
        data_id = request.POST.get('data_id')
        if data_id:
            data_to_delete = get_object_or_404(ScrapedData, id=data_id, user=user)
            data_to_delete.delete()
            messages.success(request, 'Data deleted successfully')
            return redirect('profile')
        
    display_data = [
        {
            'id': data.id,
            'data': str(data.data)[:200]
        }
        for data in scraped_data
    ]
    
    if not display_data:
        messages.error(request, "You Don't have any data to display")
        return render(request, 'profile.html')
    else:
        return render(request, 'profile.html', {'scraped_data': display_data})




def download_json(request):
    import json
    user = request.user
    try:
        scraped_data_objects = ScrapedData.objects.filter(user=user)
    except TypeError or not user:
        return HttpResponse("Bad Request")
    data_list = [data.data for data in scraped_data_objects]
    response = HttpResponse(json.dumps(data_list), content_type='application/json')
    return response




def home(request):
    return render(request, 'home.html')





@login_required
def data_detail_view(request, data_id):
    data_instance = get_object_or_404(ScrapedData, id=data_id, user=request.user)
    return render(request, 'data_detail.html', {'data_instance': data_instance})


from django.contrib.auth import update_session_auth_hash

class change_password_view(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'change_password.html', {'form': form})
    
    def post(self, request):
        user = request.user
        form = ChangePasswordForm(request.POST)
        
        if form.is_valid():
            current_password = form.cleaned_data['password']
            new_password = form.cleaned_data['new_password']
            new_password_confirmation = form.cleaned_data['new_password_confirmation']
            
            if not user.check_password(current_password):
                messages.error(request, "Incorrect current password")
                return render(request, 'change_password.html', {'form': form})
            
            if new_password != new_password_confirmation:
                messages.error(request,"Passwords Do Not Match")
                return render(request, 'change_password.html', {'form': form})
            
            
            serializer_class = ChangePasswordSerializer(data={'new_password':new_password})
            if serializer_class.is_valid():
                serializer_class.update(instance=user, validated_data=serializer_class.validated_data)
                update_session_auth_hash(request, user)
                messages.success(request, "Password updated successfully")
                return redirect('home')
            else:
                messages.error(request, serializer_class.errors)

        return render(request, 'change_password.html', {'form': form})