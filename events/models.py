#coding=utf-8
from django.db import models
from photologue.models import Gallery, Photo
from tinymce.models import HTMLField
from tinymce.widgets import TinyMCE
from django.db import connection
from django.utils import timezone
from django.core.urlresolvers import reverse

class EventManager(models.Model):
    def _dbaccess(self, isCurrent):
        op = '>' if isCurrent else '<'
        cursor = connection.cursor()
        cursor.execute("""
            SELECT * FROM events_event
            WHERE id IN 
            (SELECT event_id FROM
                (SELECT id, event_id, MAX(datetime) as datetime
                FROM events_event_date
                GROUP BY event_id) as dates
            WHERE dates.datetime < NOW());""")
        result_list = []
        for row in cursor.fetchall():
            pass
        return True

    def current_events(self):
        return self._dbaccess(True)

    def archive_events(self):
        return self._dbaccess(False)
        

class Event(models.Model):
    title = models.CharField(max_length=64, verbose_name='Titel')
    linkname = models.SlugField(help_text='Dette vises i linket: fragmentet.dk/LINKNAME', verbose_name='Linknavn')
    CATEGORY_CHOICES = (
        (0, "Forestilling"),
        (1, "Workshop"),
        (2, "Audition"),
    )
    category = models.PositiveSmallIntegerField(choices=CATEGORY_CHOICES, verbose_name='Kategori')
    event_type = models.CharField(max_length=64, null=True, blank=True, help_text='F.eks. teaterkoncert, intim koncert eller juleforestilling', verbose_name='Type')
    # description = HTMLField(widget=TinyMCE(attrs={'rows':30}), verbose_name='Beskrivelse')
    description = HTMLField(verbose_name='Beskrivelse')
    cast = HTMLField(null=True, blank=True, verbose_name='Medvirkende')
    info = HTMLField(null=True, blank=True, verbose_name='Praktisk info')
    address = models.CharField(max_length=128, null=True, blank=True, verbose_name='Adresse')
    ticket_link = models.URLField(null=True, blank=True, verbose_name='Billetlink')
    facebook_id = models.BigIntegerField(null=True, blank=True, help_text=u"<b>Udfyld kun, hvis eventet allerede er på facebook.</b> Dette er tallet i adressebaren på begivenhedens facebook-side.")
    coverimage = models.ForeignKey(Photo, default=Photo.objects.filter(title='default_cover')[0])
    galleries = models.ManyToManyField(Gallery, null=True, blank=True, verbose_name='Gallerier')
    objects = EventManager()

    def get_absolute_url(self):
        if self.alldates.latest().datetime >= timezone.now():
            return reverse('events.views.current_single', args=[self.linkname])
        else:
            return reverse('events.views.archive_single', args=[self.linkname])
            

    def last_date(self):
        print self.alldates.last()
        return self.alldates.last()

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
