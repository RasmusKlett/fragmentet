from django.db import models

class Coming_event(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField()
    sidebar = models.TextField()
    production = models.TextField()
    facebook_link = models.URLField(max_length=64)

    def __unicode__(self):
        return self.name
    class Meta:
        ordering = ['name']
