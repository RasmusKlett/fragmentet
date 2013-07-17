# Create your views here.
from django.shortcuts import render, get_object_or_404
from events.models import *
import facebook
import os
import time
from datetime import datetime
from django.core.cache import cache
from photologue.models import Gallery, Photo


def get_wall_posts():
    f = open('events/facebook_token.txt', 'r+')
    access_token = f.read()[:-1]
    graph = facebook.GraphAPI(access_token)
    posts = graph.request("126467437553756", {"fields":"posts.limit(4).fields(type,status_type,story,message,link,caption,created_time)", "locale":"da_DK"})
    data = posts["posts"]["data"]
    # Convert dates to struct_time objects
    for post in data:
        post["created_time"] = datetime.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S+0000")
    return data
    

def main(request):
    posts = cache.get('facebook_data')
    if not posts:
        try:
            posts = get_wall_posts()
            cache.set('facebook_data', posts)
        except Exception as e:
           print "FBError:", e
    event = get_object_or_404(Event,title='Backstage')
    return render(request, 'events.main.html', {'event': event, 'posts':posts})

def archive_list(request):
    return render(request, 'events.archive_list.html')

def archive_single(request):
    return render(request, 'events.archive_single.html')

def current_list(request):
    events= Event.objects.all()
    shows = events.filter(category=0)
    workshops = events.filter(category=1)
    auditions = events.filter(category=2)
    return render(request, 'events.current_list.html', {'shows':shows, 'workshops':workshops, 'auditions':auditions})

def current_single(request, event_linkname):
    event = get_object_or_404(Event,linkname=event_linkname)
    return render(request, 'events.current_single.html', {'event': event})

def show_gallery(request, event_linkname, gallery_title_slug):
    gallery = Gallery.objects.prefetch_related('photos').get(title_slug=gallery_title_slug)
    return render(request, 'events.show_gallery.html', {'linkname':event_linkname, 'gallery': gallery})
