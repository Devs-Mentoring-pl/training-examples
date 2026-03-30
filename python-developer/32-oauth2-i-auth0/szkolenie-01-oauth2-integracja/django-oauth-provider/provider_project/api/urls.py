from django.urls import path

from . import views

urlpatterns = [
    path("protected/", views.protected_resource, name="protected-resource"),
    path("public/", views.public_resource, name="public-resource"),
]
