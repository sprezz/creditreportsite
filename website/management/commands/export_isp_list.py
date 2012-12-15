# -*- coding:utf-8 -*-
from django.core.management import BaseCommand

from website.models import ISPWhiteList


class Command(BaseCommand):
    def handle(self, *args, **options):
        isp_list = ISPWhiteList.objects.values_list('name', flat=True)
        print('\n'.join(isp_list))
