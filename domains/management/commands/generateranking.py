from math import log

from django.core.management.base import BaseCommand, CommandError
from django.db.models.aggregates import Sum, Max
from django.conf import settings

from domains.models import PeerLink, UserLink


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        qs = PeerLink.objects.all()
        normalised_count_max = log(qs.aggregate(Max('count'))['count__max'] * settings.PEER_NORMALISATION_FACTOR)
        site_map = {}

        for site in qs:
            site_map[site.domain] = (log(
                site.count * settings.PEER_NORMALISATION_FACTOR) / normalised_count_max) * settings.PEER_FACTOR

        qs = UserLink.objects.all()
        normalised_count_max = log(qs.aggregate(Max('count'))['count__max'] * settings.USER_NORMALISATION_FACTOR)

        for site in qs:
            site_map[site.domain] += (log(
                site.count * settings.USER_NORMALISATION_FACTOR) / normalised_count_max) * settings.USER_FACTOR

        for key, value in site_map.items():
            value += settings.OFFSET_FACTOR
            self.stdout.write(self.style.SUCCESS(
                '{domain:40}\t{factor:2.10f}'.format(domain=key, factor=value)
            ))
