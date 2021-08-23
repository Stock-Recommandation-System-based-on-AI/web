from django.db import models
from django.conf import settings
# Create your models here.

class Stock(models.Model):
    code = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    section = models.CharField(max_length=100)
    date = models.DateTimeField()
    open = models.IntegerField(null=True)
    high = models.IntegerField(null=True)
    low = models.IntegerField(null=True)
    close = models.IntegerField(null=True)
    vol = models.IntegerField(null=True)
    value = models.IntegerField(null=True)
    n_stock = models.IntegerField(null=True)
    agg_price = models.IntegerField(null=True)
    foreign_rate = models.FloatField(null=True)
    interest_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='interst_stock', blank=True)