from django.db import models

class Album(models.Model):
    name = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    release_date = models.DateField()
    cover_image = models.ImageField(upload_to='album_covers/', blank=True, null=True)  


    def __str__(self):
        return self.name

    @property
    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return sum(rating.value for rating in ratings) / ratings.count()
        return 0

class Rating(models.Model):
    album = models.ForeignKey(Album, related_name='ratings', on_delete=models.CASCADE)
    value = models.FloatField()  

    def __str__(self):
        return f"{self.value} for {self.album.name}"


class Music(models.Model):
    album = models.ForeignKey(Album, related_name='songs', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    duration = models.DurationField()

    def __str__(self):
        return self.title

class Comment(models.Model):
    album = models.ForeignKey(Album, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment on {self.album.name} by {self.id}"


