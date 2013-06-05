# Create your views here.
from django.shortcuts import render

def mainpage(request):  
    return render(request, 'events.main.html')
