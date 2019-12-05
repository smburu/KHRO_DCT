import datetime

from django.db import models
from django.utils import timezone

class CommonInfo(models.Model):
    date_created = models.DateTimeField(
        default=timezone.now, verbose_name = 'Date Created')
    date_lastupdated = models.DateTimeField(
        default=timezone.now, verbose_name = 'Date Modified')

    class Meta:
        managed = True
        abstract = True
