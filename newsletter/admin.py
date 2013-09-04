from django.contrib import admin
from newsletter.models import *

class SubscriberAdmin(admin.ModelAdmin):
    date_hierarchy = 'join_date'
    list_display = ('email', 'join_date',)
    list_filter = ('join_date',)

admin.site.register(Subscriber, SubscriberAdmin)
