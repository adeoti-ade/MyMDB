from django.urls import path

from .views import MovieList

app_name = 'core'

urlpatterns = [
    path("movies", MovieList.as_view(), name="MovieList")
]

