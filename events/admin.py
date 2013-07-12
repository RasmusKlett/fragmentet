from django.contrib import admin
from events.models import *


class EventDateInline(admin.TabularInline):
    model = Event_date

class EventAdmin(admin.ModelAdmin):
    prepopulated_field = {'linkname':('title',)}
    radio_fields = {'category':admin.VERTICAL}
    list_filter = ('category',)
    search_fields = ['title']
    # fields = ('title', 'linkname', 'category', 'event_type', 'description', 'cast', 'info', 'address', 'ticket_link', 'facebook_id', 'coverimage', 'galleries', 'event__dates') 
    inlines= [ EventDateInline]

admin.site.register(Event, EventAdmin)
