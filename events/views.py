# Create your views here.
from django.shortcuts import render, get_object_or_404
from events.models import *

def archive(request):
    return render(request, 'events.archive.html')

def list(request):
    return render(request, 'events.list.html', {'events':Coming_event.objects.all()})

def view_event(request, event_name):
    event = get_object_or_404(Coming_event,name=event_name)
    return render(request, 'events.view_event.html', {'event': event})
