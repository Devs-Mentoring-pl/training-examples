# urls.py (główny)

from django.contrib import admin
from django.urls import path
from strawberry.django.views import GraphQLView
from blog.schema import schema

urlpatterns = [
    path("admin/", admin.site.urls),
    path("graphql/", GraphQLView.as_view(schema=schema)),
]
