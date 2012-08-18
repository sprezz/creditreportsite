# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'LandingPage'
        db.create_table('website_landingpage', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('header_content', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('body_content', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('lp_file', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('safe_lp_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('force_safe_lp', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
        ))
        db.send_create_signal('website', ['LandingPage'])

        # Adding model 'Keyword'
        db.create_table('website_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal('website', ['Keyword'])

        # Adding model 'Visitor'
        db.create_table('website_visitor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('ua', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('keyword', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('text', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('lp', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('visit_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('country_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('zip_code', self.gf('django.db.models.fields.CharField')(max_length=20, null=True, blank=True)),
            ('cloaked', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=30, null=True, blank=True)),
        ))
        db.send_create_signal('website', ['Visitor'])


    def backwards(self, orm):
        # Deleting model 'LandingPage'
        db.delete_table('website_landingpage')

        # Deleting model 'Keyword'
        db.delete_table('website_keyword')

        # Deleting model 'Visitor'
        db.delete_table('website_visitor')


    models = {
        'website.keyword': {
            'Meta': {'object_name': 'Keyword'},
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
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
            'keyword': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'lp': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ua': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'visit_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']