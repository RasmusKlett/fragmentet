from django.contrib import admin
from events.models import *


class EventDateInline(admin.TabularInline):
    model = Event_date

class EventAdmin(admin.ModelAdmin):
    prepopulated_field = {'linkname':('title',)}
    radio_fields = {'category':admin.VERTICAL}
    list_filter = ('category',)
    search_fields = ['title']
    filter_horizontal = ['galleries']
    inlines= [ EventDateInline]

admin.site.register(Event, EventAdmin)
