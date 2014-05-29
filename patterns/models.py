#Re-write of intiial mySQL schema autogenerated Django model!
# Legacy/mySQL first may be a bad idea.
# Trying datamodel in Djano first approach
# 20140422


from __future__ import unicode_literals

from django.db import models


class DesignPattern(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Pattern Name', unique=True, max_length=255)
    pictogram = models.FileField('Pattern Pictogram', upload_to='pictograms')
    author = models.CharField('Author', max_length=45, blank=True)
    contributor = models.CharField('Contributor', max_length=45, blank=True)
    
    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'design_pattern'

class Context(models.Model):
    id = models.AutoField(primary_key=True)
    parent_pattern = models.ForeignKey(DesignPattern)
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'context'



class Problem(models.Model):
    id = models.AutoField(primary_key=True)
    parent_pattern = models.ForeignKey(DesignPattern)
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'problem'


class Solution(models.Model):
    id = models.AutoField(primary_key=True)
    parent_pattern = models.ForeignKey(DesignPattern)
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'solution'


class Force(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Name', unique=True, max_length=255)
    parent_pattern = models.ForeignKey(DesignPattern)
    pictogram = models.FileField('Force Pictogram', upload_to='pictograms')
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'pattern_force'

        
class Rationale(models.Model):
    id = models.AutoField(primary_key=True)
    parent_pattern = models.ForeignKey(DesignPattern)
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'rationale'


class Diagram(models.Model):
    id = models.AutoField(primary_key=True)
    parent_pattern = models.ForeignKey(DesignPattern)
    diagram = models.FileField('Supporting Diagram', upload_to='diagrams')
    title = models.CharField('Title', max_length=255, blank=True)
    comment = models.TextField('Diagram comments', blank=True)

    def __unicode__(self):
        return self.title

    class Meta:
        db_table = 'diagram'

    
class Evidence(models.Model):
    id = models.AutoField(primary_key=True)
    parent_pattern = models.ForeignKey(DesignPattern)
    reference = models.TextField('References', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'evidence'


class RelatedWord(models.Model):
    id = models.AutoField(primary_key=True)
    force = models.ForeignKey(Force)
    word = models.CharField('Related Word', max_length=255, blank=True)

    def __unicode__(self):
        return self.word

    class Meta:
        db_table = 'force_words'

class RelatedOntologyTerm(models.Model):
    id = models.AutoField(primary_key=True)
    prefLabel = models.CharField('Label', max_length=255)
    synonyms = models.TextField('Synonyms', blank=True)
    definition = models.TextField('Defintion')
    force = models.ForeignKey(Force)
    ontology = models.URLField('Ontology')
    term = models.URLField('Term')

    BROADER = 'skos:broadMatch'
    NARROWER = 'skos:narrowMatch'
    EXACTMATCH = 'skos:exactMatch'
    CLOSEMATCH = 'skos:closeMatch'
    RELATEDMATCH = 'skos:relatedMatch'

    CHOICES = (
            (BROADER, 'Broader'),
            (NARROWER, 'Narrower'),
            (EXACTMATCH, 'Exact'),
            (CLOSEMATCH, 'Close'),
            (RELATEDMATCH, 'Related'),
        ) 
    relationship = models.CharField(max_length=25, choices=CHOICES, default=RELATEDMATCH)

    def __unicode__(self):
        return self.prefLabel

    class Meta:
        db_table = 'ontology_terms'

class WorkshopMetadata(models.Model):
    id = models.AutoField(primary_key=True)
    parent_pattern = models.ForeignKey(DesignPattern)
    media = models.FileField('File', upload_to='workshop_materials')

    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'workshop_materials'

class PatternRelation(models.Model):
    id = models.AutoField(primary_key=True)
    subject_pattern = models.ForeignKey(DesignPattern, related_name='subject_pattern', blank=True, null=True)
    linked_pattern = models.ForeignKey(DesignPattern, related_name='linked_pattern', blank=True, null=True)

    USES = 'lp:uses'
    USEDBY = 'lp:usedBy'
    UPSTREAM = 'lp:upstreamOf'
    DOWNSTREAM = 'lp:downstreamOf'
    RELATED = 'lp:relatedTo'
    INCOMPATIBLE = 'lp:incompatibleWith'

    CHOICES = (
        (USES, 'Uses'),
        (USEDBY, 'Used By'),
        (UPSTREAM, 'Upstream Of'),
        (DOWNSTREAM,'Downstream Of'),
        (RELATED, 'Related To'),
        (INCOMPATIBLE, 'Incompatible With'),
        )
    
    relationship = models.TextField('This pattern ...', max_length=50, choices = CHOICES, default=RELATED)

    def __unicode__(self):
        return self.subject_pattern.name

    class Meta:
        db_table = 'pattern_relations'