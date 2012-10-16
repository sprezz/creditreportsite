# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'OutboundLink'
        db.create_table('website_outboundlink', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=200)),
        ))
        db.send_create_signal('website', ['OutboundLink'])

        # Deleting field 'LandingPage.lp_file'
        db.delete_column('website_landingpage', 'lp_file')

        # Deleting field 'LandingPage.safe_lp_file'
        db.delete_column('website_landingpage', 'safe_lp_file')

        # Deleting field 'LandingPage.header_content'
        db.delete_column('website_landingpage', 'header_content')

        # Deleting field 'LandingPage.body_content'
        db.delete_column('website_landingpage', 'body_content')

        # Deleting field 'LandingPage.force_safe_lp'
        db.delete_column('website_landingpage', 'force_safe_lp')

        # Adding field 'LandingPage.name'
        db.add_column('website_landingpage', 'name',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10),
                      keep_default=False)

        # Adding M2M table for field index_links on 'LandingPage'
        db.create_table('website_landingpage_index_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('landingpage', models.ForeignKey(orm['website.landingpage'], null=False)),
            ('outboundlink', models.ForeignKey(orm['website.outboundlink'], null=False))
        ))
        db.create_unique('website_landingpage_index_links', ['landingpage_id', 'outboundlink_id'])

        # Adding M2M table for field safe_links on 'LandingPage'
        db.create_table('website_landingpage_safe_links', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('landingpage', models.ForeignKey(orm['website.landingpage'], null=False)),
            ('outboundlink', models.ForeignKey(orm['website.outboundlink'], null=False))
        ))
        db.create_unique('website_landingpage_safe_links', ['landingpage_id', 'outboundlink_id'])


    def backwards(self, orm):
        # Deleting model 'OutboundLink'
        db.delete_table('website_outboundlink')

        # Adding field 'LandingPage.lp_file'
        db.add_column('website_landingpage', 'lp_file',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=100),
                      keep_default=False)

        # Adding field 'LandingPage.safe_lp_file'
        db.add_column('website_landingpage', 'safe_lp_file',
                      self.gf('django.db.models.fields.files.FileField')(default=None, max_length=100),
                      keep_default=False)

        # Adding field 'LandingPage.header_content'
        db.add_column('website_landingpage', 'header_content',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10),
                      keep_default=False)

        # Adding field 'LandingPage.body_content'
        db.add_column('website_landingpage', 'body_content',
                      self.gf('django.db.models.fields.CharField')(default=None, max_length=10),
                      keep_default=False)

        # Adding field 'LandingPage.force_safe_lp'
        db.add_column('website_landingpage', 'force_safe_lp',
                      self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Deleting field 'LandingPage.name'
        db.delete_column('website_landingpage', 'name')

        # Removing M2M table for field index_links on 'LandingPage'
        db.delete_table('website_landingpage_index_links')

        # Removing M2M table for field safe_links on 'LandingPage'
        db.delete_table('website_landingpage_safe_links')


    models = {
        'website.ipban': {
            'Meta': {'object_name': 'IPBan'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.BigIntegerField', [], {'unique': 'True', 'db_index': 'True'})
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
            'ip': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'keyword': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['website.Keyword']"}),
            'lp': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'referer': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'text': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'ua': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'viewport': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'visit_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'zip_code': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['website']