from __future__ import unicode_literals

from django.db import models


class Base(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(db_index=True)
    description = models.TextField()
    active = models.BooleanField(default=True)

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.slug = slugify(self.name)

        super(test, self).save(*args, **kwargs)


class BaseOffense(Base):
    poison_damage = models.PositiveSmallIntegerField(default=0)
    fire_damage = models.PositiveSmallIntegerField(default=0)
    cold_damage = models.PositiveSmallIntegerField(default=0)
    acid_damage = models.PositiveSmallIntegerField(default=0)
    electricity_damage = models.PositiveSmallIntegerField(default=0)

    class Meta:
        abstract = True