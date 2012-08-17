from django.db import models

# Create your models here.


class LandingPage(models.Model):
    header_content = models.CharField(max_length=10)
    body_content = models.CharField(max_length=10)
    lp_file = models.CharField(max_length=100)
    safe_lp_file = models.FileField(upload_to='uploaded_templates')
    force_safe_lp = models.FileField(upload_to='uploaded_templates', blank=True, null=True)


class Keyword(models.Model):
    keyword = models.CharField('bank keyword', max_length=10)
    image = models.ImageField('bank logo', upload_to='images')
    text = models.CharField('bank text', max_length=20)
    domain = models.CharField('bank domain', max_length=20)

    def logo(self):
        x = '<img src="%s" />' % self.image.url
        return x
    logo.allow_tags = True

class Visitor(models.Model):
    ip = models.CharField(max_length = 20)
    ua = models.CharField(max_length = 100)
    keyword = models.CharField(max_length = 20)
    text = models.CharField(max_length = 20, null=True, blank=True)
    lp = models.CharField(max_length = 20, null=True, blank=True)
    visit_datetime = models.DateTimeField()
    city = models.CharField(max_length = 20, null=True, blank=True)
    state = models.CharField(max_length = 20, null=True, blank=True)
    country_code = models.CharField(max_length = 20, null=True, blank=True)
    zip_code = models.CharField(max_length = 20, null=True, blank=True)
    cloaked = models.BooleanField()
    reason = models.CharField(max_length=30, null=True, blank=True)

