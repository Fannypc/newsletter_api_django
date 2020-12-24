from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User


class Newsletter(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    image = models.CharField(max_length=50, null=True)
    target = models.ManyToManyField(User, related_name='target', blank=True)
    frequency = models.CharField(max_length=50, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    guests = models.ManyToManyField(User, related_name='guests', blank=True)
    likes = models.ManyToManyField(User, related_name='likes', blank=True)
    owner = models.ForeignKey(User, related_name='owner', on_delete=models.CASCADE, null=True)
    subscribers = models.ManyToManyField(User, related_name='subscribers', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        permissions = (
            ('is_admin', _('Is Admin')),
            ('is_user', _('Is User')),
            ('is_owner', _('Is Owner')),
            ('is_guest', _('Is Guest')),
        )
