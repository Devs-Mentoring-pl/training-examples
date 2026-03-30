from oauth2_provider.contrib.rest_framework import OAuth2Authentication, TokenHasReadWriteScope
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response


@api_view(["GET"])
@authentication_classes([OAuth2Authentication])
@permission_classes([TokenHasReadWriteScope])
def protected_resource(request):
    """Endpoint chroniony przez OAuth2 – wymaga ważnego access tokena."""
    return Response({
        "message": f"Witaj, {request.user.username}!",
        "scopes": request.auth.scope,
    })


@api_view(["GET"])
def public_resource(request):
    """Endpoint publiczny – nie wymaga tokena."""
    return Response({
        "message": "To jest zasób publiczny, dostępny dla każdego.",
    })
