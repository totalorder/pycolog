from django.db import models

class Logger(models.Model):
    name = models.CharField(max_length=512)
    regex = models.CharField(max_length=1024, default=r"(\[(error|warning|info|debug)])")

# Create your models here.
class Entry(models.Model):
    logger = models.ForeignKey(Logger, related_name="entries")
    data = models.TextField()
