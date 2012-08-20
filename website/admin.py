from django.contrib import admin
from .models import Keyword, LandingPage, Visitor


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'text', 'domain', 'logo')

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visit_datetime', 'ip', 'city', 'state', 'country_code', 'keyword', 'lp', 'cloaked', 'reason', 'text', 'ua')
    search_fields = ['ip','city','state','country_code','ua']
    ordering = ('-visit_datetime',)
    list_filter = ['reason', ]

admin.site.register(Visitor, VisitorAdmin)
admin.site.register(LandingPage)
admin.site.register(Keyword, KeywordAdmin)

