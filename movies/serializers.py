from dataclasses import fields
import movies
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import APIException  # Import APIException
from rest_framework.response import Response
from rest_framework import mixins, status

from .models import (
    Movies,
    ChildrensMovie,
    Genre,
    NewRelease,
    TYPE,
    Pricing,
    year_choices,
    RentOutMovies,
)
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
import datetime


class RentOutMoviesSerializer(ModelSerializer):
    class Meta:
        model = RentOutMovies
        fields = "__all__"


class RentMovieSerialiser(serializers.ModelSerializer):
    title = serializers.PrimaryKeyRelatedField(
        queryset=Movies.objects.filter(quantity__gt=0),
        help_text="Available movies to rent out",
    )
    return_date = serializers.DateField(
        format=None,
        input_formats=[
            "%Y-%m-%d",
        ],
    )
    price = serializers.FloatField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    number_of_days_rented = serializers.CharField(read_only=True)

    def validate(self, data):
        """validates max childrens age between 3 and 16"""
        if datetime.date.today() > data["return_date"]:
            raise serializers.ValidationError("Choose a day later than today")
        return data

    class Meta:
        model = RentOutMovies
        fields = (
            "title",
            "return_date",
            "number_of_days_rented",
            "price",
            "user",
            "returned",
        )


class PricingSerializer(ModelSerializer):
    class Meta:
        model = Pricing
        fields = "__all__"


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
        if data["max_age"] > 16:
            raise serializers.ValidationError("Maximum  age is 16 Years")

        return data

    class Meta:
        model = ChildrensMovie
        fields = [
            "max_age",
            "movie",
        ]
