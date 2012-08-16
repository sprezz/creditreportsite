from django.contrib import admin
from .models import Keyword, LandingPage, Visitor


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'text', 'domain', 'logo')

admin.site.register(Visitor)
admin.site.register(LandingPage)
admin.site.register(Keyword, KeywordAdmin)

