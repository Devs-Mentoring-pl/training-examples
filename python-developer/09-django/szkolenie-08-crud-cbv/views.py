# blog/views.py

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import Article


class ArticleListView(ListView):
    model = Article
    template_name = 'blog/home.html'
    context_object_name = 'articles'
    ordering = ['-date_posted']


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'blog/article.html'
    context_object_name = 'article'


class ArticleCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Article
    template_name = 'blog/article_form.html'
    fields = ['title', 'content']
    success_message = 'Artykuł „%(title)s" został opublikowany!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin,
                        SuccessMessageMixin, UpdateView):
    model = Article
    template_name = 'blog/article_form.html'
    fields = ['title', 'content']
    success_message = 'Artykuł został zaktualizowany!'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    template_name = 'blog/article_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        article = self.get_object()
        return self.request.user == article.author
