# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines for those models you wish to give write DB access
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

#class Author(models.Model):
#    orcid_identifier = models.CharField(primary_key=True, max_length=45)
#    first_name = models.CharField(max_length=255)
#    last_name = models.CharField(max_length=255)
#    user_name = models.CharField(max_length=45)
#    twitter_handle = models.CharField(max_length=45, blank=True)
#    email_address = models.CharField(max_length=255, blank=True)
#    class Meta:
#        managed = True
#        db_table = 'author'


class DesignPattern(models.Model):
    pattern_id = models.IntegerField(unique=True)
    pattern_name = models.CharField(primary_key=True, max_length=255)
    pattern_pictogram = models.TextField(blank=True)
    pattern_author = models.CharField(max_length=45, blank=True)
    pattern_contributor = models.CharField(max_length=45, blank=True)
    class Meta:
        managed = True
        db_table = 'design_pattern'

class Context(models.Model):
    context_id = models.IntegerField(primary_key=True)
    parent_pattern_name = models.ForeignKey('DesignPattern', db_column='parent_pattern_name')
    context_description = models.TextField(blank=True)
    class Meta:
        managed = True
        db_table = 'context'

class Problem(models.Model):
    problem_id = models.IntegerField(primary_key=True)
    parent_pattern_name = models.ForeignKey(DesignPattern, db_column='parent_pattern_name')
    problem_description = models.TextField(blank=True)
    class Meta:
        managed = True
        db_table = 'problem'
        
class Solution(models.Model):
    solution_id = models.IntegerField(primary_key=True)
    parent_pattern_name = models.ForeignKey(DesignPattern, db_column='parent_pattern_name')
    solution_description = models.TextField(blank=True)
    class Meta:
        managed = True
        db_table = 'solution'

class Force(models.Model):
    force_id = models.IntegerField(primary_key=True)
    force_name = models.CharField(unique=True, max_length=255)
    parent_pattern_name = models.ForeignKey(DesignPattern, db_column='parent_pattern_name')
    force_pictogram = models.TextField(blank=True)
    force_description = models.TextField(blank=True)
    class Meta:
        managed = True
        db_table = 'force'

        
class Rationale(models.Model):
    rationale_id = models.IntegerField(primary_key=True)
    parent_pattern_name = models.ForeignKey(DesignPattern, db_column='parent_pattern_name')
    rationale_description = models.TextField(blank=True)
    class Meta:
        managed = True
        db_table = 'rationale'

class Diagram(models.Model):
    diagram_id = models.IntegerField(primary_key=True)
    parent_pattern_name = models.ForeignKey(DesignPattern, db_column='parent_pattern_name')
    supporting_diagram = models.TextField(blank=True)
    diagram_comment = models.TextField(blank=True)
    diagram_title = models.CharField(max_length=255, blank=True)
    class Meta:
        managed = True
        db_table = 'diagram'

class Evidence(models.Model):
    evidence_id = models.IntegerField(primary_key=True)
    parent_pattern_name = models.ForeignKey(DesignPattern, db_column='parent_pattern_name')
    reference = models.TextField(blank=True)
    class Meta:
        managed = True
        db_table = 'evidence'









