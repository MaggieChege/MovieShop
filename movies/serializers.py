import movies
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Movies, ChildrensMovie, Genre, NewRelease, TYPE, year_choices
import datetime


class MovieSerializer(ModelSerializer):
    class Meta:
        model = Movies
        fields = "__all__"


class NewReleaseSerializer(ModelSerializer):
    class Meta:
        model = NewRelease
        fields = "__all__"


class ChildrenMoviesSerializer(ModelSerializer):
    class Meta:
        model = ChildrensMovie
        fields = "__all__"


class CreateNewReleaseSerializer(ModelSerializer):

    movie = serializers.PrimaryKeyRelatedField(
        queryset=Movies.objects.filter(type="New_Release")
    )

    class Meta:
        model = NewRelease
        fields = ["year_released", "movie"]


class CreateNewChildrensMovie(ModelSerializer):

    movie = serializers.PrimaryKeyRelatedField(
        queryset=Movies.objects.filter(type="Children")
    )

    def validate(self, data):
        """validates max childrens age between 3 and 16"""
        if data["max_age"] < 3 and data["max_age"] < 16:
            raise serializers.ValidationError(
                "Minimum age is 3 Years. Maximum 16 Years"
            )

        return data

    class Meta:
        model = ChildrensMovie
        fields = [
            "max_age",
            "movie",
        ]
