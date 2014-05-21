# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'RelatedOntologyTerm.synomyns'
        db.delete_column(u'ontology_terms', 'synomyns')

        # Adding field 'RelatedOntologyTerm.synonyms'
        db.add_column(u'ontology_terms', 'synonyms',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'RelatedOntologyTerm.synomyns'
        db.add_column(u'ontology_terms', 'synomyns',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)

        # Deleting field 'RelatedOntologyTerm.synonyms'
        db.delete_column(u'ontology_terms', 'synonyms')


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
        u'patterns.relatedontologyterm': {
            'Meta': {'object_name': 'RelatedOntologyTerm', 'db_table': "u'ontology_terms'"},
            'definition': ('django.db.models.fields.TextField', [], {}),
            'force': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.Force']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ontology': ('django.db.models.fields.URLField', [], {'max_length': '200'}),
            'prefLabel': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'relationship': ('django.db.models.fields.CharField', [], {'default': "u'skos:relatedMatch'", 'max_length': '25'}),
            'synonyms': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
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
        }
    }

    complete_apps = ['patterns']