from django.shortcuts import render
from django.http import Http404
from newsletter.models import *
from newsletter.forms import *

# Create your views here.
def subscribe(request):
    if not request.method == 'POST':
        raise Http404
    form = SubscriberForm(request.POST)
    if form.is_valid():
        email = form.cleaned_data['email']
        s = Subscriber(email=email)
        s.save()
    return render(request, 'newsletter.subscribed.html', {'email':email, 'subscribed':True})

def unsubscribe(request):
    if request.method == 'POST':
        form = SubscriberForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                Subscriber.objects.get(email=email)
                return render(request, 'newsletter.subscribed.html')
            except Exception:
                print Exception
    return render(request, 'newsletter.unsubscribe.html', {'subscriberForm':SubscriberForm()})
