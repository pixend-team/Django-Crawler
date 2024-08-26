from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import ScrapedData


class HomeViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('home')

    def test_get_home_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, 'home.html')
        
        
class SignupViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('signup')
        
    def test_get_signup_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        
    def test_post_signup_valid_data(self):
        data = {
            'username': 'test_username',
            'password': 'test_password',
            'email': 'test_email@example.com'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(User.objects.filter(username=data['username']).exists())
        
    def test_post_with_already_in_use_username(self):
        data = {
            'username': 'apachi',
            'password': 'testpassword',
            'email': 'test_email@example.com'
        }
        response = self.client.post(self.url, data=data)
        self.assertEqual(response.status_code, 302)



class LoginViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('login')
        self.user = User.objects.create_user(username='testuser', password='testpassword')
    
    def test_login_view_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
    
    def test_login_valid_credentials(self):
        
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        
    def test_login_invalid_credentials(self):
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid credentials')

class LogoutViewTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('logout')
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)

    def test_get_logout_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)   


class Download_test(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.csv_url = reverse('download-csv')
        self.json_url = reverse('download-json')
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.client.force_authenticate(user=self.user)
        self.scraped_data = ScrapedData.objects.create(user=self.user, data={'test_key': 'test_value'})
    
    def test_csv_download(self):
        response = self.client.get(self.csv_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], 'text/html; charset=utf-8')
    
    def test_json_download(self):
        response = self.client.get(self.json_url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/html; charset=utf-8')


class ScrapedDataListTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('get-scraped-data')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        self.user_id = self.user.pk
        self.scraped_data = ScrapedData.objects.create(user=self.user, data={'test_key': 'test_value'})
    
    def test_get_scraped_data_list(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['data'], {'test_key': 'test_value'})

class ChangePasswordViewTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('change-password')
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)
        
    def test_get_change_password_view(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'change_password.html')
        
    def test_change_password_invalid_current_password(self):
        data = {
            'password':'1223',
            'new_password':'hi-there',
            'new_password_confirmation':'hi-there'
            }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Incorrect current password')
    
    def test_change_password_invalid_new_password(self):
        data = {
            'password':'password123',
            'new_password':'hi-there',
            'new_password_confirmation':'not-hi-there'
            }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Passwords Do Not Match')
        
        
    
    def test_change_password_valid(self):
        data = {
            'password':'password123',
            'new_password':'newpassword',
            'new_password_confirmation':'newpassword'
            }
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newpassword'))

from datetime import datetime

class ScrapedDataModel(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        
    def test_scraped_data_creation(self):
        data = {'data': {'key':'key', 'value':'1'}}
        scraped_data = ScrapedData.objects.create(data=data, user=self.user)
        self.assertEqual(scraped_data.data, data)
        self.assertEqual(scraped_data.user, self.user)
        self.assertIsInstance(scraped_data.created, datetime)
    
    def test_scraped_data_retrieval(self):
        data = {'data': {'key':'key', 'value':'1'}}
        ScrapedData.objects.create(data=data, user=self.user)
        retrieved_data = ScrapedData.objects.get(user=self.user)
        self.assertEqual(retrieved_data.data, data)
        self.assertEqual(retrieved_data.user, self.user)