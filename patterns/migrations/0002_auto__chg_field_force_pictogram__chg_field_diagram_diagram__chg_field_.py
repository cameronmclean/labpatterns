# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Force.pictogram'
        db.alter_column(u'force', 'pictogram', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'Diagram.diagram'
        db.alter_column(u'diagram', 'diagram', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'DesignPattern.pictogram'
        db.alter_column(u'design_pattern', 'pictogram', self.gf('django.db.models.fields.files.FileField')(max_length=100))

    def backwards(self, orm):

        # Changing field 'Force.pictogram'
        db.alter_column(u'force', 'pictogram', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Changing field 'Diagram.diagram'
        db.alter_column(u'diagram', 'diagram', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Changing field 'DesignPattern.pictogram'
        db.alter_column(u'design_pattern', 'pictogram', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

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
        u'patterns.force': {
            'Meta': {'object_name': 'Force', 'db_table': "u'force'"},
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