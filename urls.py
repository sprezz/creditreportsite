from django.conf.urls.defaults import patterns, include, url
from app1.views import hello, current_datetime, hours_ahead, blah

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
)
