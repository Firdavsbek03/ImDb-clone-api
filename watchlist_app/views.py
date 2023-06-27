from django.shortcuts import render
from django.http import JsonResponse
from .models import Movie
from django.forms.models import model_to_dict


def movies(request):
    movies_all=Movie.objects.all()
    movies_all= {
        "movies":list(movies_all.values())
    }
    return JsonResponse(movies_all,safe=False)


def get_movie(request,pk):
    movie=Movie.objects.get(id=pk)
    movie=model_to_dict(movie)
    return JsonResponse(movie)
