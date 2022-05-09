import os
from django.shortcuts import render
from bato_app.forms import UrlForm
import re

def home(request):
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            valid_url = re.match("https://www.amazon.ae/(.*?)",form.cleaned_data["url"])
            if valid_url:
                os.system("python manage.py crawl {args}".format(args=form.cleaned_data["url"]))
    else:
        form = UrlForm()
    return render(request,'home.html',{'form':form})