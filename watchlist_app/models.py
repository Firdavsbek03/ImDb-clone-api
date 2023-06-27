from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.contrib.auth.models import User


class StreamPlatform(models.Model):
    name=models.CharField(max_length=250)
    description=models.CharField(max_length=300)
    website=models.URLField(null=True,blank=True)

    def __str__(self):
        return self.name


class Movie(models.Model):
    name=models.CharField(max_length=250)
    description=models.CharField(max_length=500)
    platform=models.ForeignKey(StreamPlatform,on_delete=models.CASCADE,blank=True,null=True,related_name='movies')
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.FloatField(default=0,null=True,blank=True)
    active=models.BooleanField(default=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Review(models.Model):
    writer=models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    rating=models.FloatField(validators=[MinValueValidator(0),MaxValueValidator(10)])
    description=models.TextField()
    active=models.BooleanField(default=True)
    movie=models.ForeignKey(Movie,on_delete=models.CASCADE,related_name='reviews')
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.rating)+"/10   |"+self.movie.name
