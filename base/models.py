from __future__ import unicode_literals

from django.db import models


class Base(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    active = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
