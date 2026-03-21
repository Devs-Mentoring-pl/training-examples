# Przyklady problemu N+1 i rozwiazania
# Uruchom w Django shell: python manage.py shell_plus --print-sql

from core.models import Mentor, Student

# -------------------------------------------------------
# Problem N+1 -- kazdy student generuje osobne zapytanie po mentora
# -------------------------------------------------------

# BAD: N+1 zapytan (1 po studentow + N po mentorow)
students = Student.objects.all()[:5]
for student in students:
    print(student.mentor.name)  # osobne zapytanie na kazdego mentora!

# -------------------------------------------------------
# Rozwiazanie 1: select_related -- dla ForeignKey i OneToOne
# Generuje SQL z JOIN, 1 zapytanie zamiast N+1
# -------------------------------------------------------

# GOOD: 1 zapytanie z JOIN
students = Student.objects.select_related("mentor")[:5]
for student in students:
    print(student.mentor.name)  # mentor juz pobrany, brak dodatkowego SQL

# -------------------------------------------------------
# Rozwiazanie 2: prefetch_related -- dla reverse FK i ManyToMany
# Generuje 2 zapytania zamiast N+1
# -------------------------------------------------------

# BAD: N+1 zapytan (1 po mentorow + N po studentow kazdego mentora)
mentors = Mentor.objects.all()[:5]
for mentor in mentors:
    print(mentor.student_set.all())  # osobne zapytanie na kazdego mentora!

# GOOD: 2 zapytania (1 po mentorow + 1 po wszystkich studentow)
mentors = Mentor.objects.prefetch_related("student_set")[:5]
for mentor in mentors:
    print(mentor.student_set.all())  # studenci juz pobrani

# -------------------------------------------------------
# Lancuchowanie select_related
# -------------------------------------------------------

# Mozna podazac za relacjami w glab:
# Student -> Mentor -> Organization (gdyby Mentor mial FK do Organization)
# students = Student.objects.select_related("mentor__organization")
