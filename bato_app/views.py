import os
from django.shortcuts import render
from bato_app.forms import UrlForm

def home(request):
    if request.method == "POST":
        form = UrlForm(request.POST)
        if form.is_valid():
            os.system("python3 manage.py crawl {args}".format(args=form.cleaned_data["url"]))
    else:
        form = UrlForm()
    return render(request,'home.html',{'form':form})