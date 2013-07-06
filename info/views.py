# Create your views here.
from django.shortcuts import render

def mainpage(request):
    return render(request, 'info.main.html')

def about(request):
    return render(request, 'info.about.html')

def archive(request):
    return render(request, 'info.archive.html')

def membership(request):
    return render(request, 'info.membership.html')

def contact(request):
    return render(request, 'info.contact.html')
