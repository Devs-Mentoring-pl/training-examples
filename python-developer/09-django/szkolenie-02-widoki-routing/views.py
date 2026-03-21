# blog/views.py

from django.shortcuts import render

# Tymczasowe dane -- docelowo beda w bazie danych
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


def home(request):
    context = {
        'title': 'Strona glowna',
        'posts': POSTS,
    }
    return render(request, 'blog/home.html', context)


def about(request):
    context = {
        'title': 'O blogu',
    }
    return render(request, 'blog/about.html', context)
