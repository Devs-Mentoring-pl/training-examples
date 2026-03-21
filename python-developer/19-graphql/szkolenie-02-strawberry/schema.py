# blog/schema.py

import strawberry
import strawberry_django
from typing import list

from .types import ArticleType, ArticleInput, ArticlePartialInput, ArticleFilter
from .permissions import IsAuthenticated


@strawberry.type
class Query:
    articles: list[ArticleType] = strawberry_django.field(filters=ArticleFilter)

    @strawberry_django.field
    def article(self, slug: str) -> ArticleType | None:
        from .models import Article

        try:
            return Article.objects.get(slug=slug, is_published=True)
        except Article.DoesNotExist:
            return None

    @strawberry.field
    def me(self, info: strawberry.types.Info) -> "UserType | None":
        from .types import UserType

        user = info.context.request.user
        if not user.is_authenticated:
            return None
        return UserType(
            id=strawberry.ID(str(user.id)),
            username=user.username,
            email=user.email,
        )


@strawberry.type
class Mutation:
    @strawberry_django.mutation(permission_classes=[IsAuthenticated])
    def create_article(self, info: strawberry.types.Info, input: ArticleInput) -> ArticleType:
        from .models import Article

        user = info.context.request.user
        article = Article.objects.create(
            title=input.title,
            slug=input.slug,
            content=input.content,
            is_published=input.is_published,
            author=user,
        )
        return article

    @strawberry_django.mutation(permission_classes=[IsAuthenticated])
    def update_article(
        self,
        info: strawberry.types.Info,
        id: strawberry.ID,
        input: ArticlePartialInput,
    ) -> ArticleType:
        from .models import Article

        user = info.context.request.user
        article = Article.objects.get(id=id, author=user)

        # Aktualizuj tylko przesłane pola
        update_fields = []
        for field_name in ["title", "slug", "content", "is_published"]:
            value = getattr(input, field_name, strawberry.UNSET)
            if value is not strawberry.UNSET:
                setattr(article, field_name, value)
                update_fields.append(field_name)

        if update_fields:
            article.save(update_fields=update_fields)

        return article

    @strawberry_django.mutation(permission_classes=[IsAuthenticated])
    def delete_article(self, info: strawberry.types.Info, id: strawberry.ID) -> bool:
        from .models import Article

        user = info.context.request.user
        deleted_count, _ = Article.objects.filter(id=id, author=user).delete()
        return deleted_count > 0


schema = strawberry.Schema(query=Query, mutation=Mutation)
