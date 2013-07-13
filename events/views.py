# Create your views here.
from django.shortcuts import render, get_object_or_404
from events.models import *
import facebook
import os
import time
from datetime import datetime

facebookdata = None

def get_wall_posts():
    f = open('events/facebook_token.txt', 'r+')
    print 1
    access_token = f.read()[:-1]
    print access_token
    print 2
    graph = facebook.GraphAPI(access_token)
    print 3
    posts = graph.request("126467437553756", {"fields":"posts.limit(4).fields(type,status_type,story,message,link,caption,created_time)", "locale":"da_DK"})
    print 5
    data = posts["posts"]["data"]
    print 6
    # Convert dates to struct_time objects
    for post in data:
        # post["created_time"] = datetime.fromtimestamp(time.mktime(time.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S+0000")))
        post["created_time"] = datetime.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S+0000")
    print 7
    return data
    

def main(request):
    posts = facebookdata
    print facebookdata
    if not facebookdata:
        try:
            posts = get_wall_posts()
        except Exception as e:
           print "FBError:", e
    event = get_object_or_404(Event,title='Backstage')
    print event.coverimage.cache_url()
    print event.coverimage.__dict__
    return render(request, 'events.main.html', {'event': event, 'posts':posts})

def archive_list(request):
    return render(request, 'events.archive_list.html')

def archive_single(request):
    return render(request, 'events.archive_single.html')

def current_list(request):
    return render(request, 'events.current_list.html', {'events':Event.objects.all()})

def current_single(request, event_linkname):
    event = get_object_or_404(Event,linkname=event_linkname)
    return render(request, 'events.current_single.html', {'event': event})
