from django.contrib import admin
from .models import Book, Recommendation

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'ratings')

@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'likes', 'created_at')
