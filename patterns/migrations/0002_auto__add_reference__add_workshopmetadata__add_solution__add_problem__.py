# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Reference'
        db.create_table(u'refs', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('kind', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('title', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('authors', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('publisher', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('journal', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('pages', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('year', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('volume', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('number', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('month', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('url', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
            ('newField', self.gf('django.db.models.fields.TextField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Reference'])

        # Adding model 'WorkshopMetadata'
        db.create_table(u'workshop_materials', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('media', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'patterns', ['WorkshopMetadata'])

        # Adding model 'Solution'
        db.create_table(u'solution', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Solution'])

        # Adding model 'Problem'
        db.create_table(u'problem', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Problem'])

        # Adding model 'PatternRelation'
        db.create_table(u'pattern_relations', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('subject_pattern', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name=u'subject_pattern', null=True, blank=True, to=orm['patterns.DesignPattern'])),
            ('linked_pattern', self.gf('django.db.models.fields.related.ForeignKey')(default=None, related_name=u'linked_pattern', null=True, blank=True, to=orm['patterns.DesignPattern'])),
            ('relationship', self.gf('django.db.models.fields.TextField')(default=u'lp:relatedTo', max_length=50)),
        ))
        db.send_create_signal(u'patterns', ['PatternRelation'])

        # Adding model 'Evidence'
        db.create_table(u'evidence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('reference', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Evidence'])

        # Adding model 'Force'
        db.create_table(u'pattern_force', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('pictogram', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Force'])

        # Adding model 'Context'
        db.create_table(u'context', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Context'])

        # Adding model 'RelatedOntologyTerm'
        db.create_table(u'ontology_terms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('prefLabel', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('synonyms', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('definition', self.gf('django.db.models.fields.TextField')()),
            ('force', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.Force'])),
            ('ontology', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('term', self.gf('django.db.models.fields.URLField')(max_length=200)),
            ('relationship', self.gf('django.db.models.fields.CharField')(default=u'skos:relatedMatch', max_length=25)),
        ))
        db.send_create_signal(u'patterns', ['RelatedOntologyTerm'])

        # Adding model 'Diagram'
        db.create_table(u'diagram', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('diagram', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('comment', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Diagram'])

        # Adding model 'Rationale'
        db.create_table(u'rationale', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('parent_pattern', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.DesignPattern'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'patterns', ['Rationale'])

        # Adding model 'DesignPattern'
        db.create_table(u'design_pattern', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('pictogram', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
            ('contributor', self.gf('django.db.models.fields.CharField')(max_length=45, blank=True)),
        ))
        db.send_create_signal(u'patterns', ['DesignPattern'])

        # Adding model 'RelatedWord'
        db.create_table(u'force_words', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('force', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['patterns.Force'])),
            ('word', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'patterns', ['RelatedWord'])


    def backwards(self, orm):
        # Deleting model 'Reference'
        db.delete_table(u'refs')

        # Deleting model 'WorkshopMetadata'
        db.delete_table(u'workshop_materials')

        # Deleting model 'Solution'
        db.delete_table(u'solution')

        # Deleting model 'Problem'
        db.delete_table(u'problem')

        # Deleting model 'PatternRelation'
        db.delete_table(u'pattern_relations')

        # Deleting model 'Evidence'
        db.delete_table(u'evidence')

        # Deleting model 'Force'
        db.delete_table(u'pattern_force')

        # Deleting model 'Context'
        db.delete_table(u'context')

        # Deleting model 'RelatedOntologyTerm'
        db.delete_table(u'ontology_terms')

        # Deleting model 'Diagram'
        db.delete_table(u'diagram')

        # Deleting model 'Rationale'
        db.delete_table(u'rationale')

        # Deleting model 'DesignPattern'
        db.delete_table(u'design_pattern')

        # Deleting model 'RelatedWord'
        db.delete_table(u'force_words')


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
            'authors': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'journal': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'kind': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'month': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'newField': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'number': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'pages': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'parent_pattern': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['patterns.DesignPattern']"}),
            'publisher': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'url': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'volume': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'year': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'})
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