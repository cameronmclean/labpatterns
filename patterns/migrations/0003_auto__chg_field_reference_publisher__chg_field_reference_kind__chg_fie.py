# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Reference.publisher'
        db.alter_column(u'refs', 'publisher', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.kind'
        db.alter_column(u'refs', 'kind', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.newField'
        db.alter_column(u'refs', 'newField', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.title'
        db.alter_column(u'refs', 'title', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.url'
        db.alter_column(u'refs', 'url', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.journal'
        db.alter_column(u'refs', 'journal', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.authors'
        db.alter_column(u'refs', 'authors', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.number'
        db.alter_column(u'refs', 'number', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.month'
        db.alter_column(u'refs', 'month', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.volume'
        db.alter_column(u'refs', 'volume', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.year'
        db.alter_column(u'refs', 'year', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

        # Changing field 'Reference.pages'
        db.alter_column(u'refs', 'pages', self.gf('django.db.models.fields.TextField')(max_length=255, null=True))

    def backwards(self, orm):

        # Changing field 'Reference.publisher'
        db.alter_column(u'refs', 'publisher', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.kind'
        db.alter_column(u'refs', 'kind', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.newField'
        db.alter_column(u'refs', 'newField', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.title'
        db.alter_column(u'refs', 'title', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.url'
        db.alter_column(u'refs', 'url', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.journal'
        db.alter_column(u'refs', 'journal', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.authors'
        db.alter_column(u'refs', 'authors', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.number'
        db.alter_column(u'refs', 'number', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.month'
        db.alter_column(u'refs', 'month', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.volume'
        db.alter_column(u'refs', 'volume', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.year'
        db.alter_column(u'refs', 'year', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

        # Changing field 'Reference.pages'
        db.alter_column(u'refs', 'pages', self.gf('django.db.models.fields.TextField')(default='', max_length=255))

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
            'Meta': {'object_name': 'Force', 'db_table': "u'pattern_force'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"}),
            'pictogram': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        u'patterns.patternrelation': {
            'Meta': {'object_name': 'PatternRelation', 'db_table': "u'pattern_relations'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linked_pattern': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'linked_pattern'", 'null': 'True', 'blank': 'True', 'to': u"orm['patterns.DesignPattern']"}),
            'relationship': ('django.db.models.fields.TextField', [], {'default': "u'lp:relatedTo'", 'max_length': '50'}),
            'subject_pattern': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'related_name': "u'subject_pattern'", 'null': 'True', 'blank': 'True', 'to': u"orm['patterns.DesignPattern']"})
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
        u'patterns.reference': {
            'Meta': {'object_name': 'Reference', 'db_table': "u'refs'"},
            'authors': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'kind': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'month': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'newField': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'number': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'pages': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"}),
            'publisher': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'volume': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.TextField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        u'patterns.relatedontologyterm': {
            'Meta': {'object_name': 'RelatedOntologyTerm', 'db_table': "u'ontology_terms'"},
            'definition': ('django.db.models.fields.TextField', [], {}),
            'force': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.Force']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ontology': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'prefLabel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'relationship': ('django.db.models.fields.CharField', [], {'default': "u'skos:relatedMatch'", 'max_length': '25'}),
            'synonyms': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'term': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        u'patterns.relatedword': {
            'Meta': {'object_name': 'RelatedWord', 'db_table': "u'force_words'"},
            'force': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.Force']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'word': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'})
        },
        u'patterns.solution': {
            'Meta': {'object_name': 'Solution', 'db_table': "u'solution'"},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"})
        },
        u'patterns.workshopmetadata': {
            'Meta': {'object_name': 'WorkshopMetadata', 'db_table': "u'workshop_materials'"},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'media': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"})
        }
    }

    complete_apps = ['patterns']