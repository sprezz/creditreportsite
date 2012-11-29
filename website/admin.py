from django.contrib import admin
from django.conf.urls.defaults import patterns, include, url
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.db import connection

from website.models import Keyword, LandingPage, Visitor, IPBan, OutboundLink
from website.helpers import iptoint, iptoint
from website.forms import IPBanAdminForm, PurchasesUploadForm


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'text', 'domain', 'logo')

admin.site.register(Keyword, KeywordAdmin)


def visitor_ban_action(modeladmin, request, queryset):
    for ip in [iptoint(x) for x in queryset.values_list('ip', flat=True)]:
        try:
            IPBan.objects.get(ip=ip)
        except IPBan.DoesNotExist:
            ban = IPBan(ip=ip)
            ban.save()

visitor_ban_action.short_description = 'Ban selected visitors'

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visit_datetime', 'ip', 'city', 'state', 'country_code', 'keyword', 'lp', 'cloaked', 'sale',
        'reason', 'viewport', 'ban_button')
    search_fields = ('ip', 'city', 'state', 'country_code', 'ua', 'text', 'keyword__keyword')
    ordering = ('-visit_datetime',)
    list_filter = ('country_code', 'sale')
    list_select_related = True
    actions = (visitor_ban_action,)

    def ban_button(self, obj):
        try:
            if IPBan.objects.filter(ip=iptoint(obj.ip)).exists():
                return '<a href="./%s/unban/">Unban</a>' % obj.id
        except ValueError:
            pass

        return '<a href="./%s/ban/">Ban</a>' % obj.id
    ban_button.allow_tags = True
    ban_button.short_description = 'Ban IP'

    def get_urls(self):
        urls = super(VisitorAdmin, self).get_urls()
        return patterns('',
            url(r'^(?P<object_id>\d+)/ban/$', self.ban, {'action': True}),
            url(r'^(?P<object_id>\d+)/unban/$', self.ban, {'action': False}),
            (r'^purchases/$', self.purchases),
            (r'^stats/ip/$', self.stats_ips),
            (r'^stats/ua/$', self.stats_ua),
        ) + urls

    def ban(self, request, object_id, action=None):
        visitor = get_object_or_404(Visitor, pk=object_id)
        ip = iptoint(visitor.ip)

        if action is True:
            try:
                IPBan.objects.get(ip=ip)
            except IPBan.DoesNotExist:
                ban = IPBan(ip=ip)
                ban.save()
        else:
            IPBan.objects.filter(ip=ip).delete()

        return redirect(request.META.get('HTTP_REFERER', '../..'))

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

    def purchases(self, request):
        if request.POST:
            form = PurchasesUploadForm(request.POST)
            if form.is_valid():
                lines = [x.strip() for x in form.cleaned_data['text'].splitlines()]
                items_cnt = Visitor.objects.filter(text__in=lines).update(sale=True)

                messages.success(request, 'Purchases list was uploaded successfully. %d visitors was updated.' % items_cnt)

                return HttpResponseRedirect('..')

        else:
            form = PurchasesUploadForm()

        context = {
            'form': form,
        }

        return render_to_response('admin/website/visitor/purchases.html', context)

admin.site.register(Visitor, VisitorAdmin)

admin.site.register(OutboundLink)
admin.site.register(LandingPage)


class IPBanAdmin(admin.ModelAdmin):
    form = IPBanAdminForm

admin.site.register(IPBan, IPBanAdmin)
