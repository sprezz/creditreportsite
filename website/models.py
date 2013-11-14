import random
import string
from datetime import datetime
from django.db import models

import config
from website.helpers import iptoint
from website import settings as app_settings


US = 'US'
UK = 'UK'
UA = 'UA'

COUNTRY_CHOICES = (
    (US, US),
    (UK, UK),
    (UA, UA),
)


class OutboundLink(models.Model):#{{{
    url = models.URLField()

    def __unicode__(self):
        return self.url#}}}


class LandingPage(models.Model):
    name = models.CharField(max_length=10, help_text='Name of the folder with safe and index.html templates')
    country = models.CharField(max_length=2, default=US, choices=COUNTRY_CHOICES)

    index_links = models.ManyToManyField(OutboundLink, verbose_name='Links for a index page',
                                         related_name='lp_index')
    safe_links = models.ManyToManyField(OutboundLink, verbose_name='Links for a safe page',
                                        related_name='lp_safe')

    def __unicode__(self):
        return self.name

    def random_index_link(self):
        try:
            return self.index_links.all().order_by('?')[0]
        except IndexError:
            return None

    def random_safe_link(self):
        try:
            return self.safe_links.all().order_by('?')[0]
        except IndexError:
            return None


class Keyword(models.Model):
    keyword = models.CharField('bank keyword', max_length=10, unique=True)
    image = models.ImageField('bank logo', upload_to='images')
    text = models.CharField('bank text', max_length=100)
    domain = models.CharField('bank domain', max_length=100)
    country = models.CharField(max_length=2, default=US, choices=COUNTRY_CHOICES)

    def __unicode__(self):
        return self.keyword

    def logo(self):
        x = '<img src="%s" />' % self.image.url
        return x

    logo.allow_tags = True


class Visitor(models.Model):
    ip = models.CharField(max_length=20, db_index=True)
    ua = models.CharField(max_length=100)
    keyword = models.ForeignKey(Keyword)
    text = models.CharField(max_length=20, null=True, blank=True, db_index=True)  # Note the `db_index` parameter
    lp = models.CharField(max_length=20, null=True, blank=True)
    visit_datetime = models.DateTimeField(db_index=True)
    visited = models.BooleanField(default=False)
    city = models.CharField(max_length=20, null=True, blank=True)
    state = models.CharField(max_length=20, null=True, blank=True)
    country_code = models.CharField(max_length=20, null=True, blank=True)
    zip_code = models.CharField(max_length=20, null=True, blank=True)
    cloaked = models.BooleanField()
    sale = models.BooleanField(default=False)
    reason = models.CharField(max_length=30, null=True, blank=True)
    viewport = models.CharField(max_length=15, null=True, blank=True)
    referer = models.CharField(max_length=255, null=True, blank=True)
    organization = models.CharField(max_length=255, null=True, blank=True)
    isp = models.CharField(max_length=255, null=True, blank=True)
    query_string = models.CharField(max_length=255, blank=True, null=True)

    def generate_subid(self):
        while True:
            self.text = ''.join([random.choice(string.ascii_letters + string.digits) for i in range(15)])

            if Visitor.objects.filter(text=self.text).exists():
                continue

    def is_legitimate(self):
        dt3 = datetime.datetime.now() - datetime.timedelta(days=3)
        dt5 = datetime.datetime.now() - datetime.timedelta(days=5)

        if self.city.lower() in app_settings.CITIES:
            return 'city'
        elif self.state.lower() in app_settings.STATES:
            return 'region_name'
        elif not self.country_code.lower() in app_settings.ALLOWED_COUNTRY:
            return 'country_code'
        elif self.country_code.upper() != self.keyword.country:
            return 'wrong bank country_code'
        elif Visitor.objects.filter(ip=self.ip, visit_datetime__gte=dt3).count() >= 3:
            return 'visted already'
        elif self.ip and IPBan.objects.filter(ip=iptoint(self.ip)).exists():
            return 'ip'
        elif Visitor.objects.filter(ip=self.ip, visit_datetime__gte=dt5).exclude(keyword=self.keyword_id).exists():
            return 'another bank'

        return ''

    class Meta:
        ordering = ['-visit_datetime']

    def save(self, *args, **kwargs):
        if self.id is None:
            self.visit_datetime = datetime.now()
            self.reason = self.is_legitimate()
            self.cloaked = bool(self.reason)
        super(Visitor, self).save(*args, **kwargs)


class IPBan(models.Model):#{{{
    ip = models.BigIntegerField(db_index=True, unique=True)

    def __unicode__(self):
        from website.helpers import inttoip


        return inttoip(self.ip)#}}}


class ISPWhiteList(models.Model):#{{{
    name = models.CharField(max_length=100, db_index=True, unique=True)

    def __unicode__(self):
        return self.name#}}}

