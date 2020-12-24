from django.db import models
from newsletters.models import Newsletter


class Tag(models.Model):
    name = models.CharField(max_length=50)
    slug = models.CharField(max_length=50)
    creation_date = models.DateTimeField(auto_now_add=True)
    newsletters = models.ManyToManyField(Newsletter, related_name='tags', blank=True)

    def __str__(self):
        return self.name
