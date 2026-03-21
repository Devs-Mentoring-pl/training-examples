# blog/admin.py

from django.contrib import admin
from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title", "author", "date_posted"]
    list_filter = ["author", "date_posted"]
    search_fields = ["title", "content"]
    ordering = ["-date_posted"]              # domyślne sortowanie: od najnowszych
    list_per_page = 25                       # 25 rekordów na stronę
    date_hierarchy = "date_posted"           # nawigacja po datach na górze
