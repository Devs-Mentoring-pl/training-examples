# Szkolenie 2: Widoki, routing i szablony

Kod z szkolenia Django nr 2 -- widoki (FBV i CBV), routing URL, szablony z dziedziczeniem, pliki statyczne i Bootstrap 5.3.

## Pliki

- `views.py` -- widoki funkcyjne (FBV) z render() i kontekstem
- `views_cbv.py` -- widoki klasowe (CBV) z TemplateView
- `urls_blog.py` -- routing aplikacji blog (FBV)
- `urls_blog_cbv.py` -- routing aplikacji blog (CBV)
- `urls_project.py` -- routing glowny projektu z include()
- `templates/blog/base.html` -- szablon bazowy z Bootstrap 5.3 i nawigacja
- `templates/blog/home.html` -- strona glowna z lista postow
- `templates/blog/about.html` -- strona "O blogu"
- `static/blog/base.css` -- style CSS aplikacji

## Kluczowe koncepty

- Trzypoziomowy routing: views.py -> app/urls.py -> project/urls.py
- Dziedziczenie szablonow: `{% extends %}` i `{% block %}`
- Tag `{% url 'name' %}` zamiast hardkodowanych sciezek
- Tag `{% load static %}` i `{% static 'path' %}` dla plikow statycznych
- Bootstrap 5.3 (bez jQuery, prefix `data-bs-`)
