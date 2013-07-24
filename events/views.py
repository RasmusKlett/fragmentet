# Create your views here.
from django.shortcuts import render, get_object_or_404
from events.models import *
import facebook
import os
import time
from datetime import datetime
from django.core.cache import cache
from photologue.models import Gallery, Photo


def get_viewstrings(is_archive):
    if is_archive:
        return ('events.views.archive_single', 'events.views.archive_list',)
    else:
        return ('events.views.current_single', 'events.views.current_list',)


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
    print audition
    return render(request, 'events.main.html', {'event': event, 'posts':posts, 'audition':audition})

def archive_list(request):
    return current_list(request, True)
#    events= Event.objects.filter(alldates__datetime__lt=datetime.now())
#    shows = events.filter(category=0)
#    workshops = events.filter(category=1)
#    auditions = events.filter(category=2)
#    return render(request, 'events.current_list.html', {'shows':shows, 'workshops':workshops, 'auditions':auditions, 'current':True})

def archive_single(request, event_linkname):
    return current_single(request, event_linkname, True)

def current_list(request, archive=False):
    if archive:
        events= Event.objects.filter(alldates__datetime__lt=datetime.now())
    else:
        events= Event.objects.filter(alldates__datetime__gte=datetime.now())
    shows = events.filter(category=0)
    workshops = events.filter(category=1)
    auditions = events.filter(category=2)
    single_view, list_view = get_viewstrings(archive)
    print 'archive: ', archive
    print single_view, list_view
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
    single_view, list_view = get_viewstrings(archive)
    return render(request, 'events.current_single.html', {
        'event': event,
        'single_view':single_view,
        'list_view':list_view
        })
