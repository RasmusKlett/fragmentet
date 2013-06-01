from django.shortcuts import render

def mainpage(request):
    if 'HTTP_X_REQUESTED_WITH' in request.META :
        if request.META['HTTP_X_REQUESTED_WITH'] == 'XMLHttpRequest':
            return render(request, 'core.main.html', {'selected_template':'dynbase.html'})
    return render(request, 'core.main.html')
