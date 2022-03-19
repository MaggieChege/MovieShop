from urllib import response

from authentication.serializers import UserSerializer
from django.db.models import Prefetch
from django.db.utils import IntegrityError
from django.http import Http404
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status
from rest_framework.exceptions import APIException  # Import APIException
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    ListCreateAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ChildrensMovie, Movies, NewRelease, Pricing, RentOutMovies
from .serializers import (
    ChildrenMoviesSerializer,
    CreateNewChildrensMovie,
    CreateNewReleaseSerializer,
    MovieSerializer,
    NewReleaseSerializer,
    PricingSerializer,
    RentOutMoviesSerializer,
    RentMovieSerialiser,
)


class MovieListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Movies.objects.all()
    serializer_class = MovieSerializer
    pagination_class = PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
    ]

    def list(self, request):
        queryset = self.get_queryset()
        movies_serializer = MovieSerializer(queryset, many=True)
        if request.user.is_authenticated:
            user = request.user
            serializer = UserSerializer(user)
            response_list = {"movies": movies_serializer.data, "user": serializer.data}
            return Response(response_list)
        return Response(movies_serializer.data)


class MovieCreateView(CreateAPIView):
    serializer_class = MovieSerializer
    permisssion_classes = (IsAdminUser,)


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


class NewreleaseCreateView(CreateAPIView):
    serializer_class = CreateNewReleaseSerializer


class ChildrenMoviesView(ListAPIView):
    queryset = ChildrensMovie.objects.all()
    lookup_field = "max_age"
    serializer_class = ChildrenMoviesSerializer


class CreateChildrensMoviesView(CreateAPIView):
    serializer_class = CreateNewChildrensMovie

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except IntegrityError as error:
            raise APIException(detail=error)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PricingListView(ListAPIView):
    queryset = Pricing.objects.filter()
    serializer_class = PricingSerializer
    pagination_class = PageNumberPagination
    filter_backends = [
        DjangoFilterBackend,
    ]


class AddPricingDetailView(CreateAPIView, mixins.UpdateModelMixin):
    serializer_class = PricingSerializer


class RentOutMoviesListView(ListCreateAPIView):
    queryset = RentOutMovies.objects.all()
    serializer_class = RentMovieSerialiser

    def create(self, request, *args, **kwargs):
        serializer = RentMovieSerialiser(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RentOutView(ListAPIView):
    queryset = RentOutMovies.objects.filter()
    serializer_class = RentOutMoviesSerializer
