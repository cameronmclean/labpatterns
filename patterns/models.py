#Re-write of intiial mySQL schema autogenerated Django model!
# Legacy/mySQL first may be a bad idea.
# Trying datamodel in Djano first approach
# 20140422


from __future__ import unicode_literals

from django.db import models


class DesignPattern(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField('Pattern Name', unique=True, max_length=255)
    pictogram = models.ImageField('Pattern Pictogram', upload_to='pictograms')
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
    pictogram = models.ImageField('Force Pictogram', upload_to='pictograms')
    description = models.TextField('Description', blank=True)
    
    def __unicode__(self):
        return self.parent_pattern.name

    class Meta:
        db_table = 'force'

        
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
    diagram = models.ImageField('Supporting Diagram', upload_to='diagrams')
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









