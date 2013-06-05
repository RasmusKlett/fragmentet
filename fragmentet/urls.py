from django.conf.urls import patterns, include, url
#from fragmentet.views import hello, current_datetime, hours_ahead
# from events import views
import events.views
import core.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
    url(r'^$', core.views.mainpage),
    url(r'^events$', events.views.mainpage),
    #url(r'^hello/$', hello),
    #url(r'^time/$', current_datetime),
    #url(r'^time/plus/(\d{1,2})/$', hours_ahead),

    # Examples:
    # url(r'^$', 'fragmentet.views.home', name='home'),
    # url(r'^fragmentet/', include('fragmentet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
