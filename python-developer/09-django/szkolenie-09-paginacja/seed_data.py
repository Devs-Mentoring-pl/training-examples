# Skrypt do uruchomienia w Django shell: python manage.py shell

from blog.models import Article
from django.contrib.auth.models import User

author = User.objects.first()

for i in range(5):
    Article.objects.create(
        title=f"Artykul testowy #{i + 1}",
        content=f"Tresc artykulu testowego numer {i + 1}.",
        author=author,
    )

print(f"Lacznie artykulow: {Article.objects.count()}")
