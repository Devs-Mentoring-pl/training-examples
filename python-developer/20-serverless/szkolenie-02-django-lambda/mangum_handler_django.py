"""
Szkolenie 2 – Mangum handler dla Django (ASGI).

Mangum opakowuje aplikację ASGI Django i tłumaczy
event API Gateway na żądanie ASGI.
"""

from mangum import Mangum
from myproject.asgi import application

# Mangum opakowuje aplikację ASGI Django
# i tłumaczy event API Gateway → żądanie ASGI
handler = Mangum(application, lifespan="off")
