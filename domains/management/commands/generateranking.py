from math import log
import re

from django.core.management.base import BaseCommand, CommandError
from django.db.models.aggregates import Sum, Max
from django.conf import settings

from ._parse_to_xml import Parser
from domains.models import PeerLink, UserLink

"""
Formula use for computation is 
log(peer_site_count*peer_normalization_factor)/log(max(peer_site_count)*peer_normalization_factor)*peer_factor + log(user_site_count*user_normalization_factor)/log(max(user_site_count)*user_normalization_factor)*user_factor + 0.7
"""


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
            site_map[key] += settings.OFFSET_FACTOR
            # remove www from start if any
            xkey = re.sub('^www.', '', key) + '/*'
            formatted_string = '{domain}\t_cse_e3hycfajgt0\t{factor:1.6f}'.format(
                domain=xkey, factor=value + settings.OFFSET_FACTOR)
            self.stdout.write(self.style.SUCCESS(formatted_string))
        xml_parser = Parser(label='_cse_e3hycfajgt0')
        xml_parser.parse(site_map)
        xml_parser.write_file()
