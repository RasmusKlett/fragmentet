# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from events.models import *
import facebook
import os
import time
from datetime import datetime
from django.core.cache import cache
from photologue.models import Gallery, Photo
from django.db.models import Max
from django.utils import timezone




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
    audition = Event.objects.filter(category=2).latest('alldates')
    return render(request, 'events.main.html', {'event': event, 'posts':posts, 'audition':audition})

def archive_list(request):
    return current_list(request, True)

def archive_single(request, event_linkname):
    return current_single(request, event_linkname, True)

def current_list(request, archive=False):
    if archive:
        single_view, list_view = ('events.views.archive_single', 'events.views.archive_list',)
        events = Event.objects.annotate(max_date=Max('alldates__datetime')).filter(max_date__lt=timezone.now())
    else:
        single_view, list_view = ('events.views.current_single', 'events.views.current_list',)
        events = Event.objects.annotate(max_date=Max('alldates__datetime')).filter(max_date__gte=timezone.now())
    shows = events.filter(category=0)
    workshops = events.filter(category=1)
    auditions = events.filter(category=2)
    return render(request, 'events.current_list.html', {
        'shows':shows, 
        'workshops':workshops, 
        'auditions':auditions, 
        'current': not archive,
        'single_view': single_view,
        'list_view': list_view,
    })

def current_single(request, event_linkname, archive=False):
    event = get_object_or_404(Event,linkname=event_linkname)
    return render(request, 'events.current_single.html', {
        'event': event
        })

def direct_event(request, event_linkname):
    event_linkname = event_linkname.lower()
    event = Event.objects.get(linkname=event_linkname)
    if event:
        return redirect(event, permanent=True)
    else:
        raise Http404
