from rest_framework import serializers
from .models import Movie, Rating


class MoviesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ("id", "title", "description")


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ("id", "stars", "user", "movie")
