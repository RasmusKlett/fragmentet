# Create your views here.
from django.shortcuts import render, get_object_or_404
from events.models import *
import facebook
import os
import time

facebookdata = None

def get_wall_posts():
    f = open('events/facebook_token.txt', 'r+')
    access_token = f.read()[:-1]
    graph = facebook.GraphAPI(access_token)
    posts = graph.request("126467437553756", {"fields":"posts.fields(type,status_type,story,message,link,caption,created_time)", "locale":"da_DK"})
    data = posts["posts"]["data"]
    # Convert dates to struct_time objects
    for post in data:
        post["created_time"] = time.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S+0000")
    return data
    

def main(request):
    posts = None
    try:
        posts = get_wall_posts()
    except e:
       print e
    event = get_object_or_404(Coming_event,name='Backstage')
    return render(request, 'events.main.html', {'event': event, 'posts':posts})

def archive_list(request):
    return render(request, 'events.archive_list.html')

def archive_single(request):
    return render(request, 'events.archive_single.html')

def current_list(request):
    return render(request, 'events.current_list.html', {'events':Coming_event.objects.all()})

def current_single(request, event_name):
    event = get_object_or_404(Coming_event,name=event_name)
    return render(request, 'events.current_single.html', {'event': event})
