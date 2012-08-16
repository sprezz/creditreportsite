# Create your views here.

from django.shortcuts import render_to_response, HttpResponse
from .models import Keyword, LandingPage

def get_landing_page(request, bank_keyword, lp='lp5'):
    try:
        bank = Keyword.objects.get(keyword=bank_keyword)
    except Keyword.DoesNotExist:
        return HttpResponse('Bank not found in system')
    logo = bank.image.url
    return render_to_response('%s/index.html' % lp,locals())
