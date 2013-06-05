from django.shortcuts import render

def check_ajax(request):
    if 'HTTP_X_REQUESTED_WITH' in request.META :
        if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
            return {'selected_template':'dynbase.html'}
    return {}

def mainpage(request):
    return render(request, 'core.main.html')
