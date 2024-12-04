from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlbumViewSet, MusicViewSet, album_comments, rate_album, protected_view
from .views import CustomAuthToken
from rest_framework.authtoken.views import ObtainAuthToken
from .views import CustomObtainAuthToken, logout



router = DefaultRouter()
router.register(r'albums', AlbumViewSet)
router.register(r'music', MusicViewSet)

urlpatterns = [
    
    path('', include(router.urls)),
    
    path('albums/<int:album_id>/rate/', rate_album, name='rate-album'),
    
    path('albums/<int:album_id>/comments/', album_comments, name='album-comments'),

    path('api/token-auth/', CustomObtainAuthToken.as_view(), name='token-auth'),

    path('logout/', logout, name='logout'),


]

