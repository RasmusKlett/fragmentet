from django.http import Http404
from newsletter.forms import SubscriberForm
from events.models import *
from info.models import *
import facebook
import os
import time
from datetime import datetime
from django.core.cache import cache
from photologue.models import Gallery, Photo
from django.db.models import Max, Min
from django.utils import timezone
from django.shortcuts import get_object_or_404, render
from django.core.exceptions import ObjectDoesNotExist
import re


def get_wall_posts():
    """Loads newsfeed from Facebook."""
    f = open('events/facebook_token.txt', 'r+') # load token from local file
    access_token = f.read()[:-1] # Strip trailing newline
    graph = facebook.GraphAPI(access_token)
    response = graph.request("126467437553756", {"fields":"posts.limit(4).fields(type,status_type,story,message,link,caption,created_time)", "locale":"da_DK"})
    posts = response["posts"]["data"]
    # Convert dates to struct_time objects
    for post in posts:
        post["created_time"] = datetime.strptime(post["created_time"], "%Y-%m-%dT%H:%M:%S+0000")
    return posts


def main(request):
    """Shows mainpage"""
    posts = cache.get('facebook_data')
    if not posts:
        try:
            posts = get_wall_posts()
            cache.set('facebook_data', posts)
        except Exception as e:
           print "FBError:", e
    event = None
    try:
        event = Event.objects.select_related().annotate(min_date=Min('alldates__datetime'), max_date=Max('alldates__datetime')).filter(category=0, max_date__gte=datetime.today()).latest('min_date')
    except ObjectDoesNotExist:
        pass
    if not event:
        page = Infopage.objects.select_related().get(title='Inaktiv Forside')
        event = {
            'is_inactive': True,
            'description': page.texts.get(title='Beskrivelse').content,
            'title': re.sub('<[^<]+?>', '', page.texts.get(title='Overskrift').content),
            'coverimage': page.images.all()[0],
            'linkname': 'info.views.about'
        }
    else:
        if event.min_date == event.max_date:
            event.date = event.min_date
    audition = None
    try:
        audition = Event.objects.annotate(date=Min('alldates__datetime')).filter(category=2).latest('alldates')
    except ObjectDoesNotExist:
        pass
    return render(request, 'events.main.html', {
        'event': event, 
        'posts':posts, 
        'audition':audition,
        'subscriberForm': SubscriberForm()
    })

def _view_list(request, isArchive):
    """Returns listview of events"""
    if isArchive:
        single_view, list_view = ('events.views.archive_single', 'events.views.archive_list',)
        events = Event.objects.annotate(min_date=Min('alldates__datetime'), max_date=Max('alldates__datetime')).filter(max_date__lt=timezone.now())
    else:
        single_view, list_view = ('events.views.current_single', 'events.views.current_list',)
        events = Event.objects.annotate(min_date=Min('alldates__datetime'), max_date=Max('alldates__datetime')).filter(max_date__gte=timezone.now())
    shows = []
    workshops = []
    auditions = []
    for event in events:
        if event.max_date == event.min_date:
            event.max_date = False
        if event.category == 0:
            shows.append(event)
        elif event.category == 1:
            workshops.append(event)
        elif event.category == 2:
            auditions.append(event)
    return render(request, 'events.current_list.html', {
        'shows':shows, 
        'workshops':workshops, 
        'auditions':auditions, 
        'current': not isArchive,
        'single_view': single_view,
        'list_view': list_view,
    })

def current_list(request):
    """returns listview of current events."""
    return _view_list(request, False)

def archive_list(request):
    """returns listview of archived events."""
    return _view_list(request, True)


def _view_single(request, event_linkname, isArchive):
    """returns listview of a single event."""
    event = Event.objects.select_related().prefetch_related('galleries').get(linkname=event_linkname)
    if not event:
        raise Http404
    for gallery in event.galleries.all():
        gallery.sample4 = lambda: gallery.sample(4)
    return render(request, 'events.current_single.html', {
        'current': not isArchive,
        'event': event
    })

def current_single(request, event_linkname):
    """returns listview of a single current event."""
    return _view_single(request, event_linkname, False)

def archive_single(request, event_linkname):
    """returns listview of a single archived event."""
    return _view_single(request, event_linkname, True)

def direct_event(request, event_linkname):
    """Handles requests to /linkname """
    event_linkname = event_linkname.lower()
    event = Event.objects.get(linkname=event_linkname)
    if event:
        return redirect(event, permanent=True)
    else:
        raise Http404
