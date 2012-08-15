# Create your views here.
from django.http import HttpResponse, Http404
from django.template.loader import get_template
from django.template import Context
from django.shortcuts import render_to_response
import datetime

def hello(request):
    return HttpResponse("Hello world")

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><head><title>Current DT</title></head><body>it is now %s</body></html>" % now
    t = get_template('datetime.html')
    html = t.render(Context({'current_date':now}))
    return HttpResponse(html)

def current_datetime(request):
    current_date = datetime.datetime.now()
    return render_to_response('datetime.html', current_date)

def hours_ahead(request, offset):
    try:
        offset = int(offset)
    except ValueError:
        raise Http404
    dt = datetime.datetime.now() + datetime.timedelta(offset)
    html = "In %s hours it will be %s" % (offset, dt)
    return HttpResponse(html)