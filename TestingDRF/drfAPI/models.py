from django.db import models


class Artist(models.Model):
    name = models.CharField(max_length=166)
    email = models.EmailField(blank=True, null=True)
    bio = models.TextField(null=True, blank=True, help_text="Give some info about artist")
    song_total = models.IntegerField(blank=True, null=True)
    choices = models.TextField(choices=[('1', 'Choice 1'), ('2', 'Choice 2')], blank=True, null=True)
    favorite = models.BooleanField(default=False)
    last_modified = models.DateField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Album(models.Model):
    title = models.CharField(max_length=100)
    released_on = models.DateTimeField(blank=True, null=True)
    artists = models.ManyToManyField('Artist')


class Song(models.Model):
    title = models.CharField(max_length=100)
    album = models.ForeignKey('Album', on_delete=models.CASCADE)
