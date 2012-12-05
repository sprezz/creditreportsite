# -*- coding:utf-8 -*-
from django.core.management import BaseCommand

from website.models import Visitor, ISPWhiteList


class Command(BaseCommand):
    def handle(self, *args, **options):
        existing_isps = ISPWhiteList.objects.values_list('name', flat=True)
        print(existing_isps)

        new_isp_name_list = set(Visitor.objects.exclude(isp__in=existing_isps, isp__isnull=True).values_list('isp', flat=True))
        print(new_isp_name_list)

        for i, name in enumerate(new_isp_name_list):
            print(i, name)
            if name:
                ISPWhiteList.objects.create(name=name)