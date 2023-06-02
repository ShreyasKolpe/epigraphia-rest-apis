# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import django.contrib.gis.db.models as gis_models


class SourceText(models.Model):
    source_text_id = models.AutoField(primary_key=True)
    source_text_title = models.TextField()
    source_text_subtitle = models.TextField(blank=True, null=True)
    source_text_author = models.TextField(blank=True, null=True)
    source_text_series = models.TextField(blank=True, null=True)
    source_text_volume = models.TextField(blank=True, null=True)
    source_text_publisher = models.TextField(blank=True, null=True)
    source_text_publication_place = models.TextField(blank=True, null=True)
    source_text_publication_date = models.DateField(blank=True, null=True)
    created_by = models.CharField(blank=True, null=True, max_length=100)
    last_modified_by = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        str = self.source_text_title
        if self.source_text_series and self.source_text_volume:
            str = "{} {}, {}".format(self.source_text_series, self.source_text_volume, self.source_text_title)
        elif self.source_text_volume:
            str = "{} {}".format(self.source_text_title, self.source_text_volume)
        return str

    class Meta:
        managed = False
        db_table = 'source_text'


class SourceTextChapter(models.Model):
    source_text_chapter_id = models.AutoField(primary_key=True)
    source_text_chapter_title = models.TextField()
    source_text = models.ForeignKey(SourceText, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(blank=True, null=True, max_length=100)
    last_modified_by = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(self.source_text.source_text_title, self.source_text_chapter_title)

    class Meta:
        managed = False
        db_table = 'source_text_chapter'


class Location(gis_models.Model):
    location_id = gis_models.AutoField(primary_key=True)
    location_name = gis_models.TextField(null=False)
    coordinates = gis_models.PointField()
    created_by = gis_models.CharField(blank=True, null=True, max_length=100)
    last_modified_by = gis_models.CharField(blank=True, null=True, max_length=100)
    created_at = gis_models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_at = gis_models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.location_name

    class Meta:
        managed = False
        db_table = 'location'


class Inscription(models.Model):
    inscription_id = models.AutoField(primary_key=True)
    source_text_inscription_number = models.IntegerField()
    source_text_chapter = models.ForeignKey(SourceTextChapter, on_delete=models.SET_NULL, null=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(blank=True, null=True, max_length=100)
    last_modified_by = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return "{}, {}".format(str(self.source_text_chapter), self.source_text_inscription_number)

    class Meta:
        managed = False
        db_table = 'inscription'


class Transliteration(models.Model):
    transliteration_id = models.AutoField(primary_key=True)
    header = models.TextField(blank=True, null=True)
    transliteration = models.TextField(blank=True, null=True)
    footnotes = models.TextField(blank=True, null=True)
    inscription = models.ForeignKey(Inscription, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(blank=True, null=True, max_length=100)
    last_modified_by = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.inscription)

    class Meta:
        managed = False
        db_table = 'transliteration'


class Translation(models.Model):
    translation_id = models.AutoField(primary_key=True)
    header = models.TextField(blank=True, null=True)
    translation = models.TextField(blank=True, null=True)
    footnotes = models.TextField(blank=True, null=True)
    inscription = models.ForeignKey(Inscription, on_delete=models.SET_NULL, null=True)
    created_by = models.CharField(blank=True, null=True, max_length=100)
    last_modified_by = models.CharField(blank=True, null=True, max_length=100)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    last_modified_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return str(self.inscription)

    class Meta:
        managed = False
        db_table = 'translation'


class InscriptionJoined(models.Model):
    source_text_id = models.IntegerField()
    source_text_series = models.TextField(blank=True, null=True)
    source_text_volume = models.TextField(blank=True, null=True)
    source_text_title = models.TextField()
    source_text_subtitle = models.TextField(blank=True, null=True)
    source_text_author = models.TextField(blank=True, null=True)
    source_text_publisher = models.TextField(blank=True, null=True)
    source_text_publication_place = models.TextField(blank=True, null=True)
    source_text_publication_date = models.DateField(blank=True, null=True)
    source_text_chapter_id = models.IntegerField()
    source_text_chapter_title = models.TextField()
    source_text_inscription_number = models.IntegerField()
    inscription_id = models.IntegerField(primary_key=True)
    translation_header = models.TextField(blank=True, null=True)
    translation = models.TextField(blank=True, null=True)
    translation_footnotes = models.TextField(blank=True, null=True)
    transliteration_header = models.TextField(blank=True, null=True)
    transliteration = models.TextField(blank=True, null=True)
    transliteration_footnotes = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'inscription_joined_view'
