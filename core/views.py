from django.shortcuts import render
from photologue.models import Gallery

def check_ajax(request):
    if 'HTTP_X_REQUESTED_WITH' in request.META :
        if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
            return {'selected_template':'dynbase.html'}
    return {}


def error404(request):
    return render(request, 'core.error404.html')


def error500(request):
    return render(request, 'core.error500.html')

def show_gallery(request, event_linkname, gallery_title_slug):
    gallery = Gallery.objects.prefetch_related('photos').get(title_slug=gallery_title_slug)
    return render(request, 'core.show_gallery.html', {'linkname':event_linkname, 'gallery': gallery})
