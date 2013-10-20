# -*- coding:utf-8 -*-
import datetime
from django.core.management import BaseCommand
from django.db import connection, transaction

from website.models import Visitor


class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args:
            date, count = (datetime.date.today() - datetime.timedelta(days=14)).strftime('%Y-%m-%d'), 50
        elif len(args) == 1:
            date, count = args[0], 50
        else:
            date, count = args

        cursor = connection.cursor()
        cursor.execute("select count(*) from website_visitor where date(visit_datetime) < '%s'" % date)
        total = cursor.fetchall()[0][0]
        deleted = 0
        left = 1
        while left:
            left = cursor.execute("delete from website_visitor where date(visit_datetime) < '%s' limit %s" % (date, count))
            transaction.commit_unless_managed()
            deleted += left
            print('deleted %s of %s' % (deleted, total))


