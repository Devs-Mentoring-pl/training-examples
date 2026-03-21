# blog/types.py

import strawberry
import strawberry_django
from strawberry import auto

from . import models


@strawberry_django.type(models.Article)
class ArticleType:
    id: auto
    title: auto
    slug: auto
    content: auto
    is_published: auto
    created_at: auto
    updated_at: auto
    author: "UserType"


@strawberry.type
class UserType:
    id: strawberry.ID
    username: str
    email: str


# --- Input types ---


@strawberry_django.input(models.Article)
class ArticleInput:
    title: auto
    slug: auto
    content: auto
    is_published: auto = False  # wartość domyślna


@strawberry_django.input(models.Article, partial=True)
class ArticlePartialInput:
    title: auto
    slug: auto
    content: auto
    is_published: auto


# --- Filters ---


@strawberry_django.filters.filter(models.Article, lookups=True)
class ArticleFilter:
    title: auto
    is_published: auto
    author: "UserFilter"
    created_at: auto


@strawberry_django.filters.filter(models.User, lookups=True)
class UserFilter:
    username: auto
