from django.conf.urls import patterns, include, url
#from fragmentet.views import hello, current_datetime, hours_ahead
# from events import views
import events.views
import info.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
    url(r'^$', info.views.mainpage),
    url(r'^aktuelt/?$', events.views.list),
    url(r'^aktuelt/(\w+)/?$', events.views.view_event),
    url(r'^teatret/?$', info.views.about),
    url(r'^arkiv/?$', events.views.archive),
    url(r'^medlemskab/?$', info.views.membership),
    url(r'^kontakt/?$', info.views.contact),


    # Examples:
    # url(r'^$', 'fragmentet.views.home', name='home'),
    # url(r'^fragmentet/', include('fragmentet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
