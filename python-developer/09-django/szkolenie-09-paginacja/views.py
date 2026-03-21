# blog/views.py

from django.views.generic import ListView
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']
    paginate_by = 4  # maksymalnie 4 artykuly na strone
