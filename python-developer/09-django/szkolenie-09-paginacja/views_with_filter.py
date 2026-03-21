# blog/views.py -- wersja z django-filter

from django_filters.views import FilterView
from .models import Article
from .filters import ArticleFilter


class ArticleListView(FilterView):
    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']
    paginate_by = 4
    filterset_class = ArticleFilter
