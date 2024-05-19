from django.urls import path
from .views import GoogleBooksAPIView, RecommendationListCreateAPIView, index

urlpatterns = [
    path('', index, name='index'),
    path('books/', GoogleBooksAPIView.as_view(), name='google-books'),
    path('recommendations/', RecommendationListCreateAPIView.as_view(), name='recommendations'),
]