# blog/views.py -- wersja z Class-Based Views

from django.views.generic import TemplateView

POSTS = [
    {
        'title': 'Pierwszy post',
        'author': 'Jan Kowalski',
        'content': 'Tresc pierwszego artykulu na blogu.',
        'date': '20 marca 2026',
    },
    {
        'title': 'Drugi post',
        'author': 'Anna Nowak',
        'content': 'Tresc drugiego artykulu na blogu.',
        'date': '21 marca 2026',
    },
]


class HomeView(TemplateView):
    template_name = 'blog/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Strona glowna'
        context['posts'] = POSTS
        return context


class AboutView(TemplateView):
    template_name = 'blog/about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'O blogu'
        return context
