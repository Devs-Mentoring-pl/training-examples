"""
Szkolenie 2 – Mangum handler dla FastAPI.
"""

from mangum import Mangum
from main import app  # Twoja aplikacja FastAPI

handler = Mangum(app)
