#coding=utf-8
from django.db import models
from photologue.models import Gallery, Photo
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE


class Event(models.Model):
    title = models.CharField(max_length=64, verbose_name='Titel')
    linkname = models.SlugField(help_text='Dette vises i linket: fragmentet.dk/LINKNAME', verbose_name='Linknavn')
    CATEGORY_CHOICES = (
        (0, "Forestilling"),
        (1, "Workshop"),
        (2, "Audition"),
    )
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES, verbose_name='Kategori')
    event_type = models.CharField(max_length=64, null=True, blank=True, help_text='F.eks. teaterkoncert, julekoncert eller ', verbose_name='Type')
    # description = HTMLField(widget=TinyMCE(attrs={'rows':30}), verbose_name='Beskrivelse')
    description = HTMLField(verbose_name='Beskrivelse')
    cast = HTMLField(null=True, blank=True, verbose_name='Medvirkende')
    info = HTMLField(null=True, blank=True, verbose_name='Praktisk info')
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='Adresse')
    ticket_link = models.URLField(null=True, blank=True, verbose_name='Billetlink')


    facebook_id = models.BigIntegerField(null=True, blank=True, help_text=u"<b>Udfyld kun, hvis eventet allerede er på facebook.</b> Dette er tallet i adressebaren på begivenhedens facebook-side.")
    coverimage = models.ForeignKey(Photo, default=Photo.objects.filter(title='default_cover')[0])
    galleries = models.ManyToManyField(Gallery, null=True, blank=True, verbose_name='Gallerier')

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = 'Begivenhed'
        verbose_name_plural = 'Begivenheder'
        ordering = ['title']
        get_latest_by = 'event__dates'


class Event_date(models.Model):
    event = models.ForeignKey(Event, related_name='alldates')
    datetime = models.DateTimeField(verbose_name='Tilføj mindst startdatoen')
    class Meta:
        verbose_name = 'Dato'
        verbose_name_plural = 'Datoer'
        get_latest_by = 'datetime'
        ordering = ['-datetime']
