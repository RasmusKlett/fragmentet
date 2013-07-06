# Create your views here.
from django.shortcuts import render, get_object_or_404
from events.models import *

def main(request):
    event = get_object_or_404(Coming_event,name='Backstage')
    return render(request, 'events.main.html', {'event': event})

def archive_list(request):
    return render(request, 'events.archive_list.html')

def archive_single(request):
    return render(request, 'events.archive_single.html')

def current_list(request):
    return render(request, 'events.current_list.html', {'events':Coming_event.objects.all()})

def current_single(request, event_name):
    event = get_object_or_404(Coming_event,name=event_name)
    return render(request, 'events.current_single.html', {'event': event})
