from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    release_date = models.DateField()

    def __str__(self):
        return self.name

class Music(models.Model):
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.DurationField()

    def __str__(self):
        return self.title

