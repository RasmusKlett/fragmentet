from django.contrib import admin
from info.models import *


class InfotextInline(admin.TabularInline):
    model = Infotext
    extra = 0

class InfopageAdmin(admin.ModelAdmin):
    inlines = [InfotextInline]
    filter_horizontal = ['images']

admin.site.register(Infopage, InfopageAdmin)
