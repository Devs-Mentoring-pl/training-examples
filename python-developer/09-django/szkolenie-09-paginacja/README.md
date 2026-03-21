# Szkolenie 9: Paginacja

Kod z szkolenia Django nr 9 -- paginacja z ListView, nawigacja w szablonie, django-filter.

## Pliki

- `views.py` -- ArticleListView z paginate_by = 4
- `views_with_filter.py` -- wersja z FilterView (django-filter)
- `filters.py` -- ArticleFilter (filtrowanie po autorze)
- `templates/blog/pagination.html` -- nawigacja paginacyjna z Bootstrap 5 (+-3 strony)
- `seed_data.py` -- skrypt do tworzenia danych testowych w Django shell

## Kluczowe koncepty

- paginate_by w ListView -- jedyny atrybut potrzebny do wlaczenia paginacji
- page_obj -- obiekt z informacjami o biezacej stronie (number, has_previous, has_next)
- is_paginated -- zmienna kontekstowa do warunkowego wyswietlania nawigacji
- Filtr |add:'-3' -- dynamiczne ograniczanie wyswietlanych numerow stron
- django-filter -- integracja filtrowania z paginacja
- aria-current="page" -- dostepnosc (accessibility)
