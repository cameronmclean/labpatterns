# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DesignPattern'
        db.create_table(u'design_pattern', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('pictogram', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
        ))
        db.send_create_signal(u'patterns', ['DesignPattern'])

        # Adding model 'Context'
        db.create_table(u'context', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Context'])

        # Adding model 'Problem'
        db.create_table(u'problem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Problem'])

        # Adding model 'Solution'
        db.create_table(u'solution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Solution'])

        # Adding model 'Force'
        db.create_table(u'force', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('pictogram', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Force'])

        # Adding model 'Rationale'
        db.create_table(u'rationale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Rationale'])

        # Adding model 'Diagram'
        db.create_table(u'diagram', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('diagram', self.gf('django.db.models.fields.files.ImageField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Diagram'])

        # Adding model 'Evidence'
        db.create_table(u'evidence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('reference', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Evidence'])


    def backwards(self, orm):
        # Deleting model 'DesignPattern'
        db.delete_table(u'design_pattern')

        # Deleting model 'Context'
        db.delete_table(u'context')

        # Deleting model 'Problem'
        db.delete_table(u'problem')

        # Deleting model 'Solution'
        db.delete_table(u'solution')

        # Deleting model 'Force'
        db.delete_table(u'force')

        # Deleting model 'Rationale'
        db.delete_table(u'rationale')

        # Deleting model 'Diagram'
        db.delete_table(u'diagram')

        # Deleting model 'Evidence'
        db.delete_table(u'evidence')


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
            'pictogram': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
        },
        u'patterns.diagram': {
            'Meta': {'object_name': 'Diagram', 'db_table': "u'diagram'"},
            'comment': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'diagram': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
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
        u'patterns.force': {
            'Meta': {'object_name': 'Force', 'db_table': "u'force'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"}),
            'pictogram': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'})
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