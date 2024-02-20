from django.urls import path

from .views import *

urlpatterns = [
    path('', MoviesView.as_view(), name='movie_list'),
    path('filter/', FilterMoviesView.as_view(), name='filter'),
    path('add-rating/', AddStarRating.as_view(), name='add_rating'),
    path('search/', Search.as_view(), name='search'),

    path('<slug:slug>/', MovieDetailView.as_view(), name='movie_detail'),
    path('review/<int:pk>/', AddReview.as_view(), name='add_review'),
    path('actor/<str:slug>/', ActorView.as_view(), name='actor_detail'),

]