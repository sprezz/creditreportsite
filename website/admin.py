from django.contrib import admin
from .models import Keyword, LandingPage


class KeywordAdmin(admin.ModelAdmin):
    list_display = ('keyword', 'text', 'domain', 'logo')

admin.site.register(LandingPage)
admin.site.register(Keyword, KeywordAdmin)

