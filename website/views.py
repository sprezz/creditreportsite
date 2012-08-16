# Create your views here.

from django.shortcuts import render_to_response, HttpResponse
from django.conf import settings
from .models import Keyword, LandingPage
from pygeoip import GeoIP

geoip = GeoIP(settings.GEOIP_DB_PATH)

def get_landing_page(request, bank_keyword, lp='lp5'):
    try:
        bank = Keyword.objects.get(keyword=bank_keyword)
    except Keyword.DoesNotExist:
        return HttpResponse('Bank not found in system')
    logo = bank.image.url
    return render_to_response('%s/index.html' % lp,locals())


def ip_details(request):
    ip =  request.META.get('HTTP_X_REAL_IP', '')
    geo_data = geoip.record_by_addr(ip)
    return HttpResponse(geo_data)

