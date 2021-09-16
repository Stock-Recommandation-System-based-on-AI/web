from django.db import models
from django.conf import settings
from stock.models import Stock

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_post")
    stock = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    content = models.TextField()
    predict_date = models.DateField()
    position = models.CharField(max_length=100)
    predict_price = models.IntegerField()
    current_price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
