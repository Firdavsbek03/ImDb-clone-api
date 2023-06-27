from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import generics, viewsets, permissions
from rest_framework.exceptions import ValidationError
from rest_framework import throttling

from django_filters.rest_framework import DjangoFilterBackend

from .permissions import IsAdminOrReadOnly, IsReviewWriterOrReadOnly
from watchlist_app.models import Movie, StreamPlatform, Review
from .throttling import ReviewCreateViewThrottle
from .serializers import MovieSerializer, StreamPlatformSerializer, ReviewSerializer


class UserReview(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        username = self.request.query_params.get('username')
        return Review.objects.filter(writer__username=username)


class StreamPlatformVS(viewsets.ModelViewSet):
    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


# Stream ReviewList View
class ReviewListView(generics.ListAPIView):
    def get_queryset(self, *args, **kwargs):
        return Review.objects.filter(movie=self.kwargs['pk'])

    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['writer__username', 'active']


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = [IsReviewWriterOrReadOnly]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = 'review-detail'


class ReviewCreateView(generics.CreateAPIView):
    def perform_create(self, serializer):
        pk = self.kwargs.get("pk")
        movie = Movie.objects.get(pk=pk)

        current_user = self.request.user
        user_review = Review.objects.filter(movie=movie, writer=current_user)

        if user_review.exists():
            raise ValidationError("You have already commented for that movie!")

        if not movie.vote_total:
            movie.vote_ratio = serializer.validated_data['rating']
        else:
            sum_of_ratings = sum(movie.reviews.all().values_list("rating", flat=True))
            print(sum_of_ratings)
            movie.vote_ratio = round((sum_of_ratings + serializer.validated_data['rating']) / (movie.vote_total + 1), 2)
        movie.vote_total += 1
        movie.save()

        serializer.save(movie=movie, writer=current_user)

    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]
    throttle_classes = [ReviewCreateViewThrottle, throttling.AnonRateThrottle]
    queryset = Review.objects.all()


class MovieList2(generics.ListAPIView):
    serializer_class = MovieSerializer
    queryset = Movie.objects.all()


class MovieList(APIView):
    permission_classes = [IsAdminOrReadOnly]
    throttle_classes = [throttling.AnonRateThrottle, throttling.UserRateThrottle]

    def get(self, request):
        movies = Movie.objects.all()
        movies_serialized = MovieSerializer(movies, many=True)
        return Response(movies_serialized.data)

    def post(self, request):
        serialized_data = MovieSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data)
        else:
            return Response(serialized_data.errors)


class MovieDetailView(APIView):
    permission_classes = [IsAdminOrReadOnly]

    def get(self, request, pk):
        try:
            movie = Movie.objects.get(id=pk)
        except Movie.DoesNotExist:
            return Response({"error": "Movie Not Found!"}, status=status.HTTP_404_NOT_FOUND)
        movie_serialized = MovieSerializer(movie)
        return Response(movie_serialized.data)

    def put(self, request, pk):
        movie = Movie.objects.get(id=pk)
        movie_serialized = MovieSerializer(movie, data=request.data)
        if movie_serialized.is_valid():
            movie_serialized.save()
            return Response(movie_serialized.data)
        else:
            return Response(movie_serialized.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        movie = Movie.objects.get(id=pk)
        movie.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
