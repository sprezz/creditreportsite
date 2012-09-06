# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    no_dry_run = True

    def forwards(self, orm):
        # Adding index on 'Visitor', fields ['visit_datetime']

        db.execute('DELETE FROM website_visitor;')

        db.create_index('website_visitor', ['visit_datetime'])

        db.delete_column('website_visitor', 'keyword')

        db.add_column('website_visitor', 'keyword', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Keyword'], default=0))

        # Adding index on 'Visitor', fields ['text']
        db.create_index('website_visitor', ['text'])

        # Adding unique constraint on 'Keyword', fields ['keyword']
        db.create_unique('website_keyword', ['keyword'])


    def backwards(self, orm):
        # Removing unique constraint on 'Keyword', fields ['keyword']
        db.delete_unique('website_keyword', ['keyword'])

        # Removing index on 'Visitor', fields ['text']
        db.delete_index('website_visitor', ['text'])

        # Removing index on 'Visitor', fields ['keyword']
        db.delete_index('website_visitor', ['keyword_id'])

        # Removing index on 'Visitor', fields ['visit_datetime']
        db.delete_index('website_visitor', ['visit_datetime'])

    models = {
        'website.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'keyword': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        'website.landingpage': {
            'Meta': {'object_name': 'LandingPage'},
            'body_content': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'force_safe_lp': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'header_content': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lp_file': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'safe_lp_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'website.visitor': {
            'Meta': {'ordering': "['-visit_datetime']", 'object_name': 'Visitor'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cloaked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Keyword']"}),
            'lp': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ua': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visit_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']