from django.urls import path
from .views import movies,get_movie

urlpatterns=[
    path("",movies,name="movies"),
    path("<int:pk>/",get_movie,name="movie"),

]