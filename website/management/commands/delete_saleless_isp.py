# -*- coding:utf-8 -*-
from django.core.management import BaseCommand

from website.models import Visitor, ISPWhiteList


class Command(BaseCommand):
    def handle(self, *args, **options):
        isp_with_sales = set(Visitor.objects.filter(sale=True).
                             values_list('isp', flat=True))
        isps = ISPWhiteList.objects.exclude(name__in=isp_with_sales)
        isps.delete()