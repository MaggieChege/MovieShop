"""movies URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from authentication.views import MyObtainTokenPairView, RegisterView
from movies.views import (
    ChildrenMoviesView,
    CreateChildrensMoviesView,
    MovieCreateView,
    MovieDetailView,
    MovieListView,
    PricingListView,
    NewreleaseCreateView,
    ViewReleaseListView,
    AddPricingDetailView,
    RentOutMoviesListView,
    RentOutView,
)

# from rest_framework.authtoken import views
urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", MyObtainTokenPairView.as_view()),
    # path('api-token-auth/', views.obtain_auth_token),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", RegisterView.as_view(), name="auth_register"),
    # Movies endpoints
    path("all_movies/", MovieListView.as_view()),
    path("add_movie/", MovieCreateView.as_view()),
    path("movie/<str:title>/", MovieDetailView.as_view()),
    # Childrens Movies endpoints
    path("all_children_movies/", ChildrenMoviesView.as_view()),
    path("add_children_movies/", CreateChildrensMoviesView.as_view()),
    # New Releases
    path("add_release/", NewreleaseCreateView.as_view()),
    path("all_releases/", ViewReleaseListView.as_view()),
    # Movie Pricing
    path("add_movie_pricing/", AddPricingDetailView.as_view()),
    path("movie_prices/", PricingListView.as_view()),
    # Rent out movies
    path("rent_movies/", RentOutMoviesListView.as_view()),
    path("all_rented_movies", RentOutView.as_view()),
]
