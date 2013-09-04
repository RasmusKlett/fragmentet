from django.db import models

class Subscriber(models.Model):
    email = models.EmailField(verbose_name='Email')
    join_date = models.DateField(auto_now_add=True, verbose_name='Tilmeldingsdato')
 
    def __unicode__(self):
        return self.email
 
    class Meta:
        verbose_name = 'Abonnent'
        verbose_name_plural = 'Abonnenter'
        ordering = ['join_date']
 
