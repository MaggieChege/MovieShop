# -*- coding: utf-8 -*-

# from sqlalchemy import ForeignKey, null
# from django_enumfield import enum
import datetime
from email.policy import default
from enum import Enum, auto
from pyexpat import model
from statistics import mode
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db.models import F

RATINGS = (
    ("5", "5"),
    ("4", "4"),
    ("3", "3"),
    ("2", "2"),
    ("1", "1"),
)

TYPE = (
    ("Regular", "Regular"),
    ("Children", "Children"),
    ("New_Release", "New_Release"),
)
GenreType = (
    ("Drama", "Drama"),
    ("Romance", "Romance"),
    ("Action", "Action"),
    ("Comedy", "Comedy"),
    ("Horror", "Horror"),
)


class Genre(models.Model):
    name = models.CharField(max_length=255, primary_key=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        managed = True
        db_table = "genre"


class Movies(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True)
    type = models.CharField(choices=TYPE, max_length=50)
    genre = models.CharField(choices=GenreType, max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    movie_poster = models.URLField(null=True, blank=True)
    quantity = models.IntegerField(default=1, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    popularity = models.CharField(
        choices=RATINGS,
        max_length=100,
        null=True,
        blank=True,
        help_text="Captured as Rating between 0 -5 ",
    )

    def __str__(self):
        return f"{self.title} {self.type}>"

    class Meta:
        managed = True
        db_table = "movies"


class ChildrensMovie(models.Model):
    movie = models.OneToOneField(
        Movies, on_delete=models.CASCADE, default=None, unique=True
    )
    max_age = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.movie} {self.max_age}"

    class Meta:
        managed = True
        db_table = "childrens_movie"


def year_choices():
    return [(r, r) for r in range(2010, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class NewRelease(models.Model):
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, default=None)
    year_released = models.IntegerField(choices=year_choices(), default=current_year())
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"<New Release {self.movie} {self.year_released}>"

    class Meta:
        managed = True
        db_table = "movies_new_release"
        unique_together = [["movie", "year_released"]]


class Pricing(models.Model):
    id = models.AutoField(primary_key=True)
    movie_type = models.CharField(choices=TYPE, max_length=50, unique=True)
    price = models.FloatField(null=True, blank=True, default=0)

    class Meta:
        managed = True
        db_table = "pricing"


class RentOutMovies(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.ForeignKey(Movies, on_delete=models.SET_NULL, blank=True, null=True)
    return_date = models.DateField(blank=False, null=False)
    day = models.DateField(default=datetime.date.today)
    number_of_days_rented = models.DateField(default=datetime.date.today)
    price = models.FloatField(blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    returned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        managed = True
        db_table = "rent_out_movie"


def after_saving_rent_out_movie(sender, instance, **kwargs):
    """

    Reduce the number of Movies as we have rented them out
    """
    movie_instance = Movies.objects.filter(title=instance.title.title)
    movie_instance.update(quantity=F("quantity") - 1)


post_save.connect(after_saving_rent_out_movie, sender=RentOutMovies)
