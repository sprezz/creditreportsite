from django.db import models
from settings_local import MEDIA_ROOT
from settings import TEMPLATE_DIRS

# Create your models here.


class LandingPage(models.Model):
    header_content = models.CharField(max_length=10)
    body_content = models.CharField(max_length=10)
    lp_file = models.CharField(max_length=100)
    safe_lp_file = models.FileField(upload_to=TEMPLATE_DIRS[0])
    force_safe_lp = models.FileField(upload_to=TEMPLATE_DIRS[0], blank=True, null=True)


class Keyword(models.Model):
    keyword = models.CharField('bank keyword', max_length=10)
    image = models.ImageField('bank logo', upload_to=MEDIA_ROOT)
    text = models.CharField('bank text', max_length=20)
    domain = models.CharField('bank domain', max_length=20)

    def logo(self):
        x = '<img src="/media/images/%s"' % self.image.path.split('\\')[-1]
        return x
    logo.allow_tags = True