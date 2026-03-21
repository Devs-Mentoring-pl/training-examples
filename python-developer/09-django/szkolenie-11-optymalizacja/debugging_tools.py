# Narzedzia do analizy wydajnosci ORM
# Uruchom w Django shell: python manage.py shell

# -------------------------------------------------------
# 1. connection.queries -- podglad SQL pod spodem
#    Dziala tylko gdy DEBUG = True
# -------------------------------------------------------

from core.models import Mentor
from django.db import connection

Mentor.objects.all()
print(connection.queries)
# [{'sql': 'SELECT ... FROM "core_mentor" LIMIT 21', 'time': '0.001'}]

# -------------------------------------------------------
# 2. QuerySet.explain() -- plan wykonania zapytania
# -------------------------------------------------------

print(Mentor.objects.filter(specialization="Python").explain())
# PostgreSQL: Seq Scan on core_mentor (cost=0.00..12.88 rows=4 width=108)

# Z dodatkowymi parametrami (PostgreSQL):
# print(Mentor.objects.filter(specialization="Python").explain(analyze=True, verbose=True))

# -------------------------------------------------------
# 3. shell_plus z django-extensions
#    pip install django-extensions
#    python manage.py shell_plus --print-sql
# -------------------------------------------------------

# -------------------------------------------------------
# 4. Lazy loading -- QuerySet NIE wykonuje SQL az do ewaluacji
# -------------------------------------------------------

# Brak zapytania SQL:
mentors = Mentor.objects.all()
mentors = mentors.filter(specialization="Python")
mentors = mentors.order_by("name")

# SQL wykonuje sie dopiero tutaj:
for mentor in mentors:
    print(mentor.name)
