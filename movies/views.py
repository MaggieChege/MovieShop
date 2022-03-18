from django.shortcuts import render

from .models import Movies, ChildrensMovie, NewRelease
from django.shortcuts import render
from rest_framework.generics import (
    UpdateAPIView,
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
)
from django.db.models import Prefetch

from .serializers import (
    MovieSerializer,
    NewReleaseSerializer,
    CreateNewReleaseSerializer,
    CreateNewChildrensMovie,
    ChildrenMoviesSerializer,
)
from rest_framework import mixins

from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import APIException  # Import APIException
from django_filters.rest_framework import DjangoFilterBackend
from django.db.utils import IntegrityError
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser


class MovieListView(ListAPIView):
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
    ]

    def get_user_loggedin(request):
        user = request.user
        return JsonResponse({"user": user})

    # filterset_fields=['title']


class MovieCreateView(CreateAPIView):
    serializer_class = MovieSerializer
    permisssion_classes = (IsAdminUser,)


# class GenreCreateView(CreateAPIView):
#     serializer_class = GenreSerializer


class MovieDetailView(
    RetrieveAPIView,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
):
    queryset = Movies.objects.all()
    lookup_field = "title"
    serializer_class = MovieSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class ViewReleaseListView(ListAPIView):
    queryset = NewRelease.objects.filter()
    serializer_class = NewReleaseSerializer
    pagination_class = PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
    ]
    # filterset_fields=['title']


class NewreleaseCreateView(CreateAPIView):
    # queryset = Movies.ob/jects.filter(type="New_Release")
    serializer_class = CreateNewReleaseSerializer


# class CreateChildrensMovie(CreateAPIView):
#     queryset = Movies.objects.filter(type="Children")
#     serializer_class = CreateNewChildrensMovie


class ChildrenMoviesView(ListAPIView):
    queryset = ChildrensMovie.objects.all()
    lookup_field = "max_age"
    serializer_class = ChildrenMoviesSerializer


class CreateChildrensMoviesView(CreateAPIView):
    # queryse/t = Movies.objects.filter(type="Children")
    serializer_class = CreateNewChildrensMovie

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        # breakpoint()
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError as error:
            raise APIException(detail=error)
