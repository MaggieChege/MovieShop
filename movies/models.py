# -*- coding: utf-8 -*-

from statistics import mode

# from unittest import defaultTestLoader
from django.db import models
from enum import Enum, auto

# from sqlalchemy import ForeignKey, null
# from django_enumfield import enum
import datetime


class MovieTypeEnum(Enum):
    Regular = auto()
    Children = auto()
    New_Release = auto()


class GenreTypeEnum(Enum):
    Action = auto()
    Drama = auto()
    Romance = auto()
    Comedy = auto()
    Horror = auto()
    Animation = auto()


class Movie(models.Model):
    title = models.CharField(max_length=100, unique=True, primary_key=True)
    type = models.CharField(
        max_length=max(map(len, (v.name for v in MovieTypeEnum))),
        choices=[(enum.name, enum.name) for enum in MovieTypeEnum],
        default=MovieTypeEnum.Regular.value,
        editable=False,
    )
    genre = models.CharField(
        max_length=max(map(len, (v.name for v in GenreTypeEnum))),
        choices=[(enum.name, enum.name) for enum in GenreTypeEnum],
        default=GenreTypeEnum.Action.value,
        editable=False,
    )
    description = models.CharField(max_length=100, null=True, blank=True)
    # price = models.IntegerField()
    # quantity = models.IntergerField()
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    popularity = models.IntegerField(
        null=True, blank=True, help_text="Captured as Percentage"
    )

    def __str__(self):
        return f"<Movie {self.title} {self.type}>"

    class Meta:
        managed = True
        db_table = "movie"
        unique_together = [["title", "genre"]]


class ChildrensMovie(models.Model):
    # id = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, default=None)
    max_age = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"{self.movie} {self.max_age}>"

    class Meta:
        managed = True
        db_table = "childrens_movie"


def year_choices():
    return [(r, r) for r in range(1990, datetime.date.today().year + 1)]


def current_year():
    return datetime.date.today().year


class NewRelease(models.Model):
    # id = models.IntegerField()
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING, default=None)
    year_release = models.IntegerField(choices=year_choices(), default=current_year())
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return f"<New Release {self.movie} {self.year_release}>"

    class Meta:
        managed = True
        db_table = "new_release"
