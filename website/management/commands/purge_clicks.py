# -*- coding:utf-8 -*-
from django.core.management import BaseCommand

from website.models import Visitor


class Command(BaseCommand):
    def handle(self, *args, **options):
        visits_with_sales = Visitor.objects.filter(sale=True)

        with open('ip_sales.csv', 'w') as f:
            for visit in visits_with_sales:
#                print('%s,%s' % (visit.ip, visit.visit_datetime.strftime('%Y-%m-%d')))
                f.write('%s,%s\n' % (visit.ip, visit.visit_datetime.strftime('%Y-%m-%d')))

