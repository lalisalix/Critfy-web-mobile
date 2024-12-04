from django.contrib import admin
from .models import Album, Comment, Music, Rating

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ['name', 'artist', 'release_date', 'cover_image'] 
    list_filter = ['artist', 'release_date']  
    search_fields = ['name', 'artist']  

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['album', 'text', 'created_at']  
    list_filter = ['album', 'created_at']  
    search_fields = ['text']  

@admin.register(Music)
class MusicAdmin(admin.ModelAdmin):
    list_display = ['title', 'album', 'duration']  
    list_filter = ['album']  
    search_fields = ['title']  

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ['album', 'value']  
    list_filter = ['album']  
    search_fields = ['album__name']  
