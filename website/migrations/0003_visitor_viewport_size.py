# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Visitor.viewport'
        db.add_column('website_visitor', 'viewport',
                      self.gf('django.db.models.fields.CharField')(max_length=15, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Visitor.viewport'
        db.delete_column('website_visitor', 'viewport')


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
            'viewport': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'visit_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']