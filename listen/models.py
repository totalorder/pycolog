from django.db import models

# Create your models here.
class Entry(models.Model):
    logger = models.CharField(max_length=512)
    data = models.TextField()
