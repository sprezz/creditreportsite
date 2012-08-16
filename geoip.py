# -*- coding:utf-8 -*-
from django.conf import settings

from pygeoip import GeoIP


geoip = GeoIP(settings.GEOIP_DB_PATH)

# geo_record = geoip.record_by_addr('65.74.178.253')

#    {'area_code': 916,
#     'city': u'Sacramento',
#     'country_code': 'US',
#     'country_code3': 'USA',
#     'country_name': 'United States',
#     'dma_code': 862,
#     'latitude': 38.647099999999995,
#     'longitude': -121.5418,
#     'metro_code': 'Sacramento, CA',
#     'postal_code': u'95834',
#     'region_name': u'CA',
#     'time_zone': 'America/Los_Angeles'}
