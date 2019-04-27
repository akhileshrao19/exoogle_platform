# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.

class CommonData(models.Model):
    domain = models.CharField(max_length=256, blank=False, null=False)
    ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=1)

    class Meta:
        abstract = True


class RawUserData(CommonData):
    pass


class UserLink(CommonData):
    pass


class PeerLink(CommonData):
    pass
