from rest_framework import serializers
from .models import Album, Music

class MusicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Music
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    songs = MusicSerializer(many=True, read_only=True)
    average_rating = serializers.FloatField(read_only=True)
    cover_image = serializers.ImageField(read_only=True)  
  

    class Meta:
        model = Album
        fields = ['id', 'name', 'artist', 'release_date', 'songs', 'average_rating', 'cover_image']  
