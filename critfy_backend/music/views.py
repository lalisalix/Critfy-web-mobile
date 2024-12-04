from django.shortcuts import render, redirect
from rest_framework import viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from .models import Album, Music, Comment, Rating
from .serializers import AlbumSerializer, MusicSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny



class AlbumViewSet(viewsets.ModelViewSet):

    queryset = Album.objects.all()
    serializer_class = AlbumSerializer
    permission_classes = [AllowAny]


    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'artist']  



class MusicViewSet(viewsets.ModelViewSet):
   
    queryset = Music.objects.all()
    serializer_class = MusicSerializer


@api_view(['GET', 'POST'])
def album_comments(request, album_id):
    try:
        album = Album.objects.get(id=album_id)

        if request.method == 'GET':
            comments = album.comments.all().values('text', 'created_at')
            return Response(list(comments))

        if request.method == 'POST':
            comment_text = request.data.get('comment', '').strip()

            if not comment_text:
                return Response({"error": "O comentário não pode estar vazio."}, status=400)

            Comment.objects.create(album=album, text=comment_text)
            return Response({'message': 'Comentário salvo com sucesso!'})

    except Album.DoesNotExist:
        return Response({"error": "Álbum não encontrado."}, status=404)


@api_view(['POST'])
def rate_album(request, album_id):
    
    try:
        album = Album.objects.get(id=album_id)
        rating_value = request.data.get('rating', None)

        if rating_value is None or not (0 <= float(rating_value) <= 5):
            return Response({"error": "A nota deve estar entre 0 e 5."}, status=400)

        Rating.objects.create(album=album, value=float(rating_value))

        average_rating = album.average_rating
        return Response({
            'message': 'Nota salva com sucesso!',
            'average_rating': average_rating
        })

    except Album.DoesNotExist:
        return Response({"error": "Álbum não encontrado."}, status=404)


@api_view(['GET'])
def search_albums(request):

    query = request.GET.get('q', '').strip()
    if query:
        albums = Album.objects.filter(
            Q(name__icontains=query) | Q(artist__icontains=query)
        )
    else:
        albums = Album.objects.none()  

    serializer = AlbumSerializer(albums, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_view(request):
   
    return Response({"message": f"Olá, {request.user.username}! Você está autenticado."})

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })

class CustomObtainAuthToken(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user:
           
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        return Response({'error': 'Credenciais inválidas'}, status=401)

@api_view(['POST'])
def logout(request):
   
    if request.user.is_authenticated:
        try:
            token = Token.objects.get(user=request.user)
            token.delete() 
            return Response({"message": "Logout realizado com sucesso."}, status=200)
        except Token.DoesNotExist:
            return Response({"error": "Token não encontrado."}, status=400)
    return Response({"error": "Usuário não autenticado."}, status=401)
