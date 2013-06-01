# Create your views here.
from django.shortcuts import render

def mainpage(request):
    return render(request, 'core.main.html', {'dynamic':True, 'text':'streng fra context'})
