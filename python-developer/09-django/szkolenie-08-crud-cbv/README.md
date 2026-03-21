# Szkolenie 8: CRUD z Class-Based Views

Kompletny CRUD (Create, Read, Update, Delete) z wykorzystaniem Django CBV:
ListView, DetailView, CreateView, UpdateView, DeleteView.
Obejmuje LoginRequiredMixin, UserPassesTestMixin, SuccessMessageMixin.

## Pliki

- `models.py` -- model Article z get_absolute_url()
- `views.py` -- wszystkie widoki CBV (List, Detail, Create, Update, Delete)
- `urls.py` -- routing do wszystkich widokow CRUD

## Wymagania

```bash
pip install django django-crispy-forms crispy-bootstrap5
```
