# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from . import models as domain_models


# Register your models here.

class DomainAdmin(admin.ModelAdmin):
    list_display = ('ip', 'domain', 'count')


admin.site.register(domain_models.PeerLink, DomainAdmin)
admin.site.register(domain_models.UserLink, DomainAdmin)
admin.site.register(domain_models.RawUserData, DomainAdmin)
