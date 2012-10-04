from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url('^hello/', 'app1.views.hello'),
    url('^$', 'app1.views.blah'),
    url('^time/$', 'app1.views.current_datetime'),
    url(r'^time/plus/(\d{1,2})/$', 'app1.views.hours_ahead'),

    #From new views
    url('^cr/(\w+)/$', 'website.views.landing_page'),
    url('^cr/(\w+)/(\w+)/$', 'website.views.landing_page'),
    url('^cr/(\w+)/(\w+)/index.html$', 'website.views.landing_page'),
    #Unique subid
    url('^s/(\w+)/$', 'website.views.unique_subid'),

    url('^ipdetails', 'website.views.ip_details'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    )
