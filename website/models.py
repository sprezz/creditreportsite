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