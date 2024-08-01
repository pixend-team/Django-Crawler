# forms.py
from django import forms
from django.contrib.auth.models import User

class SignUpForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)
    
    
class ChangePasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
    new_password = forms.CharField(widget=forms.PasswordInput)
    new_password_confirmation = forms.CharField(widget=forms.PasswordInput)


class CrawlForm(forms.Form):
    url = forms.URLField(label='URL', widget=forms.URLInput(attrs={'placeholder': 'Enter the URL to scrape'}))
    keys = forms.CharField(label='Keys', widget=forms.Textarea(attrs={'placeholder': 'Enter keys separated by commas'}))
    xpaths = forms.CharField(label='XPaths', widget=forms.Textarea(attrs={'placeholder': 'Enter XPaths separated by commas'}))
    
    
