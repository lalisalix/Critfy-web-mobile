from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Album, Comment, Rating
from rest_framework.authtoken.models import Token



class AlbumAPITestCase(TestCase):
    def setUp(self):
        
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.token = Token.objects.create(user=self.user)

        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        self.album = Album.objects.create(name="Test Album", artist="Test Artist", release_date="2024-01-01")


    def test_get_albums(self):
        
        response = self.client.get('/api/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Album', str(response.data))

    def test_search_album(self):
       
        response = self.client.get('/api/albums/?search=Test')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('Test Album', str(response.data))

    def test_rate_album(self):
        
        response = self.client.post(f'/api/albums/{self.album.id}/rate/', {'rating': 4})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Rating.objects.count(), 1)
        self.assertEqual(Rating.objects.first().value, 4)

    def test_add_comment(self):
       
        response = self.client.post(f'/api/albums/{self.album.id}/comments/', {'comment': 'Great album!'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().text, 'Great album!')

    def test_unauthorized_access(self):
        
        unauthenticated_client = APIClient()
        response = unauthenticated_client.get('/api/albums/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_token_auth(self):
        
        response = self.client.post('/api/token-auth/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

        token = response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = self.client.get('/api/albums/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
