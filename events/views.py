# Create your views here.
from django.shortcuts import render

def mainpage(request):  
    #for v in request.META:
    #    print v, request.META[v]
    if 'HTTP_X_REQUESTED_WITH' in request.META :
        if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
            print 'xmlhttp!'
            r = render(request, 'events.main.html', {'selected_template':'dynbase.html'})
            r.__setitem__('responseType', 'text')
            print r.items()
            r['Content-Disposition'] = 'text'
            return r

    return render(request, 'events.main.html')
