from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
import events.views
import info.views
import core.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('', 
    url(r'^$', events.views.main),
    url(r'^aktuelt/?$', events.views.current_list),
    url(r'^aktuelt/([-\w]+)/?$', events.views.current_single),
    url(r'^arkiv/?$', events.views.archive_list),
    url(r'^arkiv/([-\w]+)/?$', events.views.archive_single),
    url(r'^galleri/([-\w]+)/([-\w]+)/?$', core.views.show_gallery),
    url(r'^om-teatret/?$', info.views.about),
    url(r'^medlemskab/?$', info.views.membership),
    url(r'^kontakt/?$', info.views.contact),
    (r'^photologue/', include('photologue.urls')),
    (r'^tinymce/', include('tinymce.urls')),


    # Examples:
    # url(r'^$', 'fragmentet.views.home', name='home'),
    # url(r'^fragmentet/', include('fragmentet.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # url(r'^([-\w]+)/?$', events.views.direct_event),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'core.views.error404'
handler500 = 'core.views.error500'
