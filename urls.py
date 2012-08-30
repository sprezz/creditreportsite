from django.conf.urls.defaults import patterns, include, url
from app1.views import hello, current_datetime, hours_ahead, blah
from website.views import get_landing_page, ip_details
from website.newviews import get_landing_page as glp
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'creditreportsite.views.home', name='home'),
    # url(r'^creditreportsite/', include('creditreportsite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url('^hello/', hello),
    url('^$', blah),
    url('^time/$', current_datetime),
    url(r'^time/plus/(\d{1,2})/$', hours_ahead),
    url('^creditreport/(\w+)/$', get_landing_page),
    url('^creditreport/(\w+)/(\w+)/$', get_landing_page),
    url('^creditreport/(\w+)/(\w+)/index.html$', get_landing_page),
    url('^creditscore/(\w+)/$', get_landing_page),
    url('^creditscore/(\w+)/(\w+)/$', get_landing_page),
    url('^creditscore/(\w+)/(\w+)/index.html$', get_landing_page),


    #From new views
    url('^cr/(\w+)/$', glp),
    url('^cr/(\w+)/(\w+)/$', glp),
    url('^cr/(\w+)/(\w+)/index.html$', glp),
    url('^cr/(\w+)/$', glp),
    url('^cr/(\w+)/(\w+)/$', glp),
    url('^cr/(\w+)/(\w+)/index.html$', glp),


    url('^ipdetails', ip_details)

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
