# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Actor(models.Model):
    aid = models.AutoField(db_column='Aid', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    photopath = models.CharField(db_column='photoPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'actor'


class Actorinmovie(models.Model):
    mid = models.OneToOneField('Movie', models.DO_NOTHING, db_column='Mid', primary_key=True)  # Field name made lowercase.
    aid = models.ForeignKey(Actor, models.DO_NOTHING, db_column='Aid')  # Field name made lowercase.
    isstarring = models.IntegerField(db_column='isStarring', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'actorinmovie'
        unique_together = (('mid', 'aid'),)


class Comment(models.Model):
    cid = models.AutoField(db_column='Cid', primary_key=True)  # Field name made lowercase.
    mid = models.ForeignKey('Movie', models.DO_NOTHING, db_column='Mid', blank=True, null=True)  # Field name made lowercase.
    uid = models.ForeignKey('User', models.DO_NOTHING, db_column='Uid', blank=True, null=True)  # Field name made lowercase.
    content = models.TextField(blank=True, null=True)
    score = models.IntegerField(blank=True, null=True)
    time = models.DateTimeField(blank=True, null=True)
    likes = models.IntegerField(blank=True, null=True)
    reply2cid = models.IntegerField(db_column='reply2Cid', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'comment'


class Director(models.Model):
    did = models.AutoField(db_column='Did', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    photopath = models.CharField(db_column='photoPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    gender = models.CharField(max_length=1, blank=True, null=True)
    nationality = models.CharField(max_length=50, blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)

    class Meta:
        db_table = 'director'


class Directorsinmovie(models.Model):
    mid = models.OneToOneField('Movie', models.DO_NOTHING, db_column='Mid', primary_key=True)  # Field name made lowercase.
    did = models.ForeignKey(Director, models.DO_NOTHING, db_column='Did')  # Field name made lowercase.

    class Meta:
        db_table = 'directorsinmovie'
        unique_together = (('mid', 'did'),)


class History(models.Model):
    uid = models.OneToOneField('User', models.DO_NOTHING, db_column='Uid', primary_key=True)  # Field name made lowercase.
    mid = models.ForeignKey('Movie', models.DO_NOTHING, db_column='Mid')  # Field name made lowercase.
    time = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'history'
        unique_together = (('uid', 'mid'),)


class Movie(models.Model):
    mid = models.AutoField(db_column='Mid', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=100, blank=True, null=True)
    date = models.DateField(blank=True, null=True)
    heat = models.IntegerField(blank=True, null=True, default=0)
    brief = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True)
    coverpath = models.CharField(db_column='coverPath', max_length=255, blank=True, null=True)  # Field name made lowercase.
    duration = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'movie'


class Movietag(models.Model):
    tag = models.CharField(primary_key=True, max_length=50)
    mid = models.ForeignKey(Movie, models.DO_NOTHING, db_column='Mid')  # Field name made lowercase.
    heat = models.IntegerField(blank=True, null=True)

    class Meta:
        db_table = 'movietag'
        unique_together = (('tag', 'mid'),)


class User(models.Model):
    uid = models.AutoField(db_column='Uid', primary_key=True)  # Field name made lowercase.
    name = models.CharField(max_length=50, blank=True, null=True)
    email = models.CharField(unique=True, max_length=100, blank=True, null=True)
    passwords = models.CharField(max_length=50, blank=True, null=True)
    photopath = models.CharField(db_column='photoPath', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'user'
