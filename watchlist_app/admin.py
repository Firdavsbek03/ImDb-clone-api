from django.contrib import admin
from .models import Movie,StreamPlatform,Review


admin.site.register(Movie)
admin.site.register(StreamPlatform)
admin.site.register(Review)