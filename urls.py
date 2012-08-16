from django.conf.urls.defaults import patterns, include, url
from app1.views import hello, current_datetime, hours_ahead, blah
from website.views import get_landing_page
from settings_local import MEDIA_ROOT

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
    url('^creditreport/(\w+)/(\w+)/', get_landing_page),

    url(r'^media/images/(?P<path>.*)$', 'django.views.static.serve',
    {'document_root': MEDIA_ROOT}),
)
