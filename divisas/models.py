from django.db import models
from django.conf import settings

# Create your models here.
class Divisa(models.Model):
    nombre = models.TextField(blank=False)
    pais = models.TextField(blank=False)
    acronimo = models.TextField(blank=False)
    precio = models.FloatField(default=0.0)
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    divisa = models.ForeignKey('divisas.Divisa', related_name='votes', on_delete=models.CASCADE)

    
    
