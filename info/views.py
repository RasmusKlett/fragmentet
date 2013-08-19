# Create your views here.
from django.shortcuts import render
from info.models import Infopage

def about(request):
    page = Infopage.objects.select_related().get(title='Om Teatret')
    history = page.texts.get(title='Historie').content
    image = page.images.all()[0]
    return render(request, 'info.about.html', {
        'history': history,
        'image': image
    })

def archive(request):
    return render(request, 'info.archive.html')

def membership(request):
    page = Infopage.objects.select_related().get(title='Medlemskab')
    active = page.texts.get(title='Aktivt medlem').content
    passive = page.texts.get(title='Passivt medlem').content
    top = page.texts.get(title='Generelt top').content
    bottom = page.texts.get(title='Generelt bund').content      

    return render(request, 'info.membership.html', {
        'active': active,
        'passive': passive,
        'top': top,
        'bottom': bottom
    })

def contact(request):
    page = Infopage.objects.select_related().get(title='Kontakt')
    contacts = page.texts.get(title='Kontakter').content
    
    return render(request, 'info.contact.html', {
        'contacts': contacts
    })
