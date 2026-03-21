# api/views.py

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from blog.models import Article
from .serializers import ArticleSerializer
from .permissions import IsAuthorOrReadOnly


class ArticleViewSet(viewsets.ModelViewSet):
    """Pełny CRUD dla artykułów – jedna klasa, wszystkie metody."""
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
