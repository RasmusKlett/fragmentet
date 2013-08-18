from django.contrib import admin
from info.models import *


class InfotextInline(admin.TabularInline):
    model = Infotext
    extra = 0

class InfopageAdmin(admin.ModelAdmin):
    inlines = [InfotextInline]
    filter_horizontal = ['images']
    search_fields = ['title']
    list_display = ('title',)

admin.site.register(Infopage, InfopageAdmin)
