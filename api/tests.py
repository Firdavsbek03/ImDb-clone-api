from django.contrib.auth.models import User
from django.urls import reverse

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from watchlist_app.models import StreamPlatform,Movie,Review


class StreamPlatformTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='testuser',password='anypassword')
        self.token=Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.platform=StreamPlatform.objects.create(
            name='Netflix',
            description='The best streaming platform',
            website='https://netflix.com'
        )

    def test_platform_create(self):
        data={
            'name':'youtube',
            'description':'Very entertaining',
            'website':'https://youtube.com'
        }
        response=self.client.post(reverse('stream-platform-list'),data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_platform_list(self):
        response=self.client.get(reverse('stream-platform-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_platform_detail(self):
        response=self.client.get(reverse('stream-platform-detail',args=(self.platform.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)


class MovieTestCase(APITestCase):
    def setUp(self):
        self.user=User.objects.create_user(username='testuser',password='anypassword')
        self.token=Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.platform=StreamPlatform.objects.create(
            name='Netflix',
            description='The best streaming platform',
            website='https://netflix.com'
        )

        self.movie=Movie.objects.create(
            name="Test Movie",
            description="Test Description",
            platform=self.platform
        )

    def test_movie_create(self):
        data={
            'name':"Test Movie",
            'description':"Test Description",
            "platform":self.platform,
            'active':True
        }
        response=self.client.post(reverse('movie_list'),data=data)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)

    def test_movie_list(self):
        response=self.client.get(reverse('movie_list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_movie_detail(self):
        response=self.client.get(reverse('get_movie',args=(self.movie.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Movie.objects.get().name,"Test Movie")
        self.assertEqual(Movie.objects.count(),1)


class ReviewTestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='anypassword')
        self.token = Token.objects.get(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)
        self.platform = StreamPlatform.objects.create(
            name='Netflix',
            description='The best streaming platform',
            website='https://netflix.com'
        )

        self.movie = Movie.objects.create(
            name="Test Movie",
            description="Test Description",
            platform=self.platform
        )

        self.review=Review.objects.create(
            writer=self.user,
            rating= 8.89,
            description= 'This is a hell of test review content.',
            movie= self.movie
        )

    # def test_review_create(self):
    #     url=reverse('review-create',args=(self.movie.id,))
    #     data={
    #         "writer":self.user,
    #         'rating':8.89,
    #         'description':'This is a hell of test review content.',
    #         'movie':self.movie,
    #         'active':True
    #     }
    #     response=self.client.post(path=url,data=data)
    #     print(response.data)
    #     print(response.status_code)
    #     self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_review_create_unauth(self):
        url=reverse('review-create',args=(self.movie.id,))
        data={
            "writer":self.user,
            'rating':8.89,
            'description':'This is a hell of test review content.',
            'movie':self.movie,
            'active':True
        }
        self.client.force_authenticate(user=None)
        response=self.client.post(path=url,data=data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_review_list(self):
        response=self.client.get(reverse('review-list',args=(self.movie.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_review_detail(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_put(self):
        data = {
            'rating':9,
            'description':'This is a hell of test review content.-updated',
            'active':False
        }
        response=self.client.put(
            reverse('review-detail',args=(self.review.id,)),
            data=data
        )
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Review.objects.get().rating,9)
        self.assertEqual(Review.objects.get().description,
                         'This is a hell of test review content.-updated')
        self.assertEqual(Review.objects.get().active,False)

    def test_review_delete(self):
        response=self.client.delete(reverse("review-detail",args=(self.review.id,)))
        self.assertEqual(Review.objects.count(),0)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    def test_review_user(self):
        response=self.client.get('/api/movies/reviews/?username='+self.user.username)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
