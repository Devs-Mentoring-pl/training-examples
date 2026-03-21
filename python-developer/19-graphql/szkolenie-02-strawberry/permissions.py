# blog/permissions.py

import strawberry
from strawberry.permission import BasePermission
from strawberry.types import Info


class IsAuthenticated(BasePermission):
    message = "Musisz być zalogowany."

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context.request.user
        return user.is_authenticated


class IsStaff(BasePermission):
    message = "Wymagane uprawnienia administratora."

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context.request.user
        return user.is_authenticated and user.is_staff


class IsAuthor(BasePermission):
    message = "Tylko autor może modyfikować ten zasób."

    def has_permission(self, source, info: Info, **kwargs) -> bool:
        user = info.context.request.user
        if not user.is_authenticated:
            return False

        # Sprawdź, czy użytkownik jest autorem
        article_id = kwargs.get("id")
        if article_id:
            from blog.models import Article
            return Article.objects.filter(id=article_id, author=user).exists()

        return True
