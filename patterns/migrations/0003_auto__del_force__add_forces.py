# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Force'
        db.delete_table(u'force')

        # Adding model 'Forces'
        db.create_table(u'force', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('pictogram', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Forces'])


    def backwards(self, orm):
        # Adding model 'Force'
        db.create_table(u'force', (
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('pictogram', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Force'])

        # Deleting model 'Forces'
        db.delete_table(u'force')


    models = {
        u'patterns.context': {
            'Meta': {'object_name': 'Context', 'db_table': "u'context'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"})
        },
        u'patterns.designpattern': {
            'Meta': {'object_name': 'DesignPattern', 'db_table': "u'design_pattern'"},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'contributor': ('django.db.models.fields.CharField', [], {'max_length': '45', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'pictogram': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'patterns.diagram': {
            'Meta': {'object_name': 'Diagram', 'db_table': "u'diagram'"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'diagram': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'patterns.evidence': {
            'Meta': {'object_name': 'Evidence', 'db_table': "u'evidence'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"}),
            'reference': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'patterns.forces': {
            'Meta': {'object_name': 'Forces', 'db_table': "u'force'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"}),
            'pictogram': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'patterns.problem': {
            'Meta': {'object_name': 'Problem', 'db_table': "u'problem'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"})
        },
        u'patterns.rationale': {
            'Meta': {'object_name': 'Rationale', 'db_table': "u'rationale'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"})
        },
        u'patterns.solution': {
            'Meta': {'object_name': 'Solution', 'db_table': "u'solution'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"})
        }
    }

    complete_apps = ['patterns']