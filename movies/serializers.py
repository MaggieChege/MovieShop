from dataclasses import fields
import movies
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import APIException  # Import APIException

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
    title = serializers.PrimaryKeyRelatedField(queryset=Movies.objects.filter(quantity__gt=0), help_text="Available movies to rent out")
    return_date = serializers.DateField(
        format=None,
        input_formats=[
            "%Y-%m-%d",
        ],
    )
    price = serializers.SerializerMethodField("get_price")
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    number_of_days_rented = serializers.SerializerMethodField("get_days_rented")

    def get_days_rented(self, obj):
        return (obj.return_date - obj.day).days

    def get_price(self, obj):
        if obj.title.type == "New_Release":
            try:
                rate = Pricing.objects.get(movie_type=obj.title.type).price
                days = (obj.return_date - obj.day).days
                pricing = rate * days
            except ObjectDoesNotExist as error:
                raise APIException(detail=error)

        if obj.title.type == "Children":
            try:
                rate = Pricing.objects.get(movie_type=obj.title.type).price
                days = (obj.return_date - obj.day).days
                maximum_age = ChildrensMovie.objects.get(
                    movie__title=obj.title.title
                ).max_age
                pricing = rate * days + (maximum_age / 2)
            except ObjectDoesNotExist as error:
                raise APIException(detail=error)
        if obj.title.type == "Regular":
            try:
                rate = Pricing.objects.get(movie_type=obj.title.type).price
                days = (obj.return_date - obj.day).days
                # year_released = NewRelease.objects.get(
                #     movie__title=obj.title.title
                # ).year_released
                # breakpoint()
                pricing = rate * days
            except ObjectDoesNotExist as error:
                raise APIException(detail=error)

        if pricing < 0:

            raise serializers.ValidationError("Return day must be after today")
        return pricing

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
