import string
import random
import datetime
import urllib2

from website.models import Visitor
from website import settings as app_settings


def generate_subid():
    """Generate new `subid`, which doesn't exists in database"""

    sequence = list(string.ascii_letters + string.digits)

    while True:
        random.shuffle(sequence)
        subid = ''.join(sequence[:15])

        if not Visitor.objects.filter(text=subid).exists():
            return subid

def legitimate_visitor(ip, geo_data, v):
    if ip in app_settings.BAD_IPS:
        return 'ip'

    dt = datetime.datetime.now() - datetime.timedelta(days=1)
    dt5 = datetime.datetime.now() - datetime.timedelta(days=5)
    number_of_visits = Visitor.objects.filter(ip=ip, visit_datetime__gte=dt5).exists()
    another_bank = Visitor.objects.filter(ip=ip, visit_datetime__gte=dt5).exclude(keyword=v.keyword_id).exists()

    if number_of_visits:
        return 'visted already'
    if another_bank:
        return 'another bank'
    if geo_data.get('city','').lower() in app_settings.CITIES:
        return 'city'
    if geo_data.get('region_name','').lower() in app_settings.STATES:
        return 'region_name'
    if not geo_data.get('country_code','').lower() in app_settings.ALLOWED_COUNTRY:
        return 'country_code'

    return ''

def is_server(ip):
    """Check if IP has its own web-server"""

    try:
        urllib2.urlopen('http://%s' % ip, timeout=0.5)
    except urllib2.URLError:
        return False
    return True
