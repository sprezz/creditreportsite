from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render_to_response
from django.db import connection

from website.models import Keyword, LandingPage, Visitor


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'text', 'domain', 'logo')

admin.site.register(Keyword, KeywordAdmin)


class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visit_datetime', 'ip', 'city', 'state', 'country_code', 'keyword', 'lp', 'cloaked', 'reason', 'viewport')
    search_fields = ('ip', 'city', 'state', 'country_code', 'ua', 'keyword__keyword')
    ordering = ('-visit_datetime',)
    list_select_related = True

    def get_urls(self):
        urls = super(VisitorAdmin, self).get_urls()
        return patterns('',
            (r'^stats/ip/$', self.stats_ips),
            (r'^stats/ua/$', self.stats_ua),
        ) + urls

    def stats_ips(self, request):
        cursor = connection.cursor()
        cursor.execute('SELECT ip, COUNT(*) AS cnt FROM website_visitor GROUP BY ip ORDER BY cnt DESC LIMIT 100;')

        context = {
            'ips': cursor.fetchall(),
        }

        return render_to_response('admin/website/visitor/stats_ip.html', context)

    def stats_ua(self, request):
        cursor = connection.cursor()
        cursor.execute('SELECT ua, COUNT(*) AS cnt FROM website_visitor GROUP BY ua ORDER BY cnt DESC;')

        context = {
            'ips': cursor.fetchall(),
        }

        return render_to_response('admin/website/visitor/stats_ip.html', context)

admin.site.register(Visitor, VisitorAdmin)

admin.site.register(LandingPage)
