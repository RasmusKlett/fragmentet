from django.db import models
from tinymce.models import HTMLField
from photologue.models import Photo


class Infopage(models.Model):
    title = models.CharField(max_length=64, verbose_name='Titel')
    images = models.ManyToManyField(Photo, null=True, blank=True, verbose_name='Billeder')
    
    class Meta:
        verbose_name = 'Infoside'
        verbose_name_plural = 'Infosider'
        ordering = ['title']


class Infotext(models.Model):
    infopage = models.ForeignKey(Infopage, related_name='texts')
    title = models.CharField(max_length=64, verbose_name='Titel')
    content = HTMLField(verbose_name='Indhold')

    def __unicode__(self):
        return self.title
    class Meta:
        verbose_name = 'Tekst'
        verbose_name_plural = 'Tekster'
