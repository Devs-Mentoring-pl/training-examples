# blog/urls.py -- wersja z Class-Based Views

from django.urls import path
from .views import HomeView, AboutView

urlpatterns = [
    path('', HomeView.as_view(), name='blog-home'),
    path('about/', AboutView.as_view(), name='blog-about'),
]
