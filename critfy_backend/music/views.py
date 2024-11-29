from django.shortcuts import render
from rest_framework import viewsets
from .models import Album, Music
from .serializers import AlbumSerializer, MusicSerializer

class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()
    serializer_class = AlbumSerializer

class MusicViewSet(viewsets.ModelViewSet):
    queryset = Music.objects.all()
    serializer_class = MusicSerializer



