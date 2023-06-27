from django.urls import path,include
from rest_framework import routers
import api.views as views

# Registering a ViewSet Router
router=routers.DefaultRouter()
router.register(r"stream-platforms",viewset=views.StreamPlatformVS,basename='stream-platform')

urlpatterns = [
    path("", views.MovieList.as_view(), name="movie_list"),
    path('<int:pk>/', views.MovieDetailView.as_view(), name='get_movie'),
    path("",include(router.urls)),

    path("<int:pk>/reviews/create", views.ReviewCreateView.as_view(), name='review-create'),
    path("<int:pk>/reviews/", views.ReviewListView.as_view(), name='review-list'),
    path("reviews/<int:pk>/", views.ReviewDetailView.as_view(), name='review-detail'),

    path("reviews/",views.UserReview.as_view(),name='user-review'),
    path('list/',views.MovieList2.as_view(),name='movie-list2'),

]
