from django.contrib import admin
from .models import Keyword, LandingPage, Visitor


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'text', 'domain', 'logo')
    search_fields = ['ip','city','state','country']

class VisitorAdmin(admin.ModelAdmin):
    list_display = ('visit_datetime', 'ip', 'city', 'state', 'country_code', 'keyword', 'lp', 'cloaked', 'reason')
    ordering = ('-visit_datetime',)

admin.site.register(Visitor, VisitorAdmin)
admin.site.register(LandingPage)
admin.site.register(Keyword, KeywordAdmin)

