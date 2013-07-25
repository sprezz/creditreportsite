# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Visitor.query_string'
        db.add_column('website_visitor', 'query_string',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Visitor.query_string'
        db.delete_column('website_visitor', 'query_string')


    models = {
        'website.ipban': {
            'Meta': {'object_name': 'IPBan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'db_index': 'True'})
        },
        'website.ispwhitelist': {
            'Meta': {'object_name': 'ISPWhiteList'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100', 'db_index': 'True'})
        },
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
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'index_links': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'lp_index'", 'symmetrical': 'False', 'to': "orm['website.OutboundLink']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'safe_links': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'lp_safe'", 'symmetrical': 'False', 'to': "orm['website.OutboundLink']"})
        },
        'website.outboundlink': {
            'Meta': {'object_name': 'OutboundLink'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'website.visitor': {
            'Meta': {'ordering': "['-visit_datetime']", 'object_name': 'Visitor'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'cloaked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'country_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '20', 'db_index': 'True'}),
            'isp': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Keyword']"}),
            'lp': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'query_string': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ua': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'viewport': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'visit_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'visited': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']