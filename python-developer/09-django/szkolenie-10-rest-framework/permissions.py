# api/permissions.py

from rest_framework.permissions import BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """
    Pozwala edytować/usuwać obiekt tylko jego autorowi.
    Odczyt (GET, HEAD, OPTIONS) – dla wszystkich.
    """

    def has_object_permission(self, request, view, obj):
        # Metody bezpieczne (read-only) – dostępne dla każdego
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return True
        # Edycja/usuwanie – tylko autor
        return obj.author == request.user
