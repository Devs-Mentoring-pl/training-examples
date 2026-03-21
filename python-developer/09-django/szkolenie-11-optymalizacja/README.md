# Szkolenie 11: Optymalizacja w Django

Kod z szkolenia Django nr 11 -- problem N+1, select_related, prefetch_related, lazy loading, narzedzia debugowania.

## Pliki

- `models.py` -- modele Mentor i Student (ForeignKey) do demonstracji N+1
- `n_plus_one.py` -- przyklady problemu N+1 i rozwiazania (select_related, prefetch_related)
- `debugging_tools.py` -- connection.queries, explain(), lazy loading, shell_plus
- `settings_debug.py` -- konfiguracja Debug Toolbar, django-extensions, django-silk

## Kluczowe koncepty

- Problem N+1 -- 1 zapytanie glowne + N zapytan po powiazane obiekty
- select_related -- eager loading z JOIN dla ForeignKey i OneToOne
- prefetch_related -- eager loading z osobnym zapytaniem dla ManyToMany i reverse FK
- Lazy loading -- QuerySet nie wykonuje SQL az do ewaluacji (iteracja, len(), list())
- connection.queries -- podglad wygenerowanego SQL (tylko DEBUG=True)
- QuerySet.explain() -- plan wykonania zapytania (odpowiednik EXPLAIN w SQL)
- Django Debug Toolbar / django-silk -- narzedzia profilowania
