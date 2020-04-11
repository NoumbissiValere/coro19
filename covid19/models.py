from django.db import models

# Create your models here.


class ResponseTime(models.Model):
    method = models.CharField(max_length=10)
    path = models.CharField(max_length=80)
    status = models.IntegerField()
    time = models.CharField(max_length=100)
