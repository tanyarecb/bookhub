from django.db import models

# Create your models here.

class Book(models.Model):
    google_books_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    cover_image = models.URLField()
    ratings = models.FloatField()

class Recommendation(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.CharField(max_length=100)
    comment = models.TextField()
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
