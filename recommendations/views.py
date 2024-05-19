from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Book, Recommendation
from .serializers import BookSerializer, RecommendationSerializer
import requests
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class GoogleBooksAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Search books using Google Books API",
        manual_parameters=[
            openapi.Parameter('search', openapi.IN_QUERY, description="Query string for searching books", type=openapi.TYPE_STRING)
        ],
        responses={200: "Successful Response"}
    )
    def get(self, request, *args, **kwargs):
        query = request.GET.get('search')
        if not query:
            return Response({"error": "Query parameter 'search' is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        response = requests.get(f'https://www.googleapis.com/books/v1/volumes?q={query}')
        if response.status_code != 200:
            return Response({"error": "Failed to fetch data from Google Books API"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        books = response.json().get('items', [])
        
        for item in books:
            volume_info = item.get('volumeInfo', {})
            book, created = Book.objects.get_or_create(
                google_books_id=item['id'],
                defaults={
                    'title': volume_info.get('title', 'No title'),
                    'author': ', '.join(volume_info.get('authors', [])),
                    'description': volume_info.get('description', 'No description'),
                    'cover_image': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                    'ratings': volume_info.get('averageRating', 0),
                }
            )
        
        return Response(books, status=status.HTTP_200_OK)

class RecommendationListCreateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Retrieve a list of recommendations",
        responses={200: RecommendationSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        recommendations = Recommendation.objects.all()
        serializer = RecommendationSerializer(recommendations, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_description="Create a new recommendation",
        request_body=RecommendationSerializer,
        responses={201: RecommendationSerializer, 400: 'Bad Request'}
    )
    def post(self, request, *args, **kwargs):
        book_id = request.data.get('book_id')
        book = Book.objects.filter(id=book_id).first()
        
        if not book:
            return Response({"error": "Book not found"}, status=status.HTTP_400_BAD_REQUEST)
        
        recommendation_data = {
            'book': book.id,
            'user': request.data.get('user'),
            'comment': request.data.get('comment'),
            'likes': request.data.get('likes', 0)
        }
        
        serializer = RecommendationSerializer(data=recommendation_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
    return render(request, 'index.html')
