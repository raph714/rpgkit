from __future__ import unicode_literals

from django.db import models
from django.utils.text import slugify


class Base(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(db_index=True)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(Base, self).save(*args, **kwargs)

    def __unicode__(self):
       return self.name
