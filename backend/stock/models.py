from django.db import models
from django.conf import settings
# Create your models here.

class Stock(models.Model):
    id = models.CharField(primary_key=True, max_length=100)
    symbol_id = models.CharField(max_length=100)
    container_id = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100, blank=True)
    probability = models.FloatField()
    interest_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interest_stock', blank=True)