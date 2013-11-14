from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^settings/', include('livesettings.urls')),
)

urlpatterns += patterns('website.views',
    #From new views
    url('^(?:cr|creditscore|creditreport)/(\w+)/$', 'landing_page'),
    url('^(?:cr|creditscore|creditreport)/(\w+)/(\w+)/$', 'landing_page'),
    url('^(?:cr|creditscore|creditreport)/(\w+)/(\w+)/index.html$', 'landing_page'),

    #Unique subid
    url('^s/(\w+)/$', 'unique_subid', name='unique_subid'),

    url('^fail/$', 'fail', name='unique_subid'),

)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        url(r'^media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT}),
        url(r'^static/(?P<path>.*)$', 'serve', {'document_root': settings.STATIC_ROOT}),
    )
