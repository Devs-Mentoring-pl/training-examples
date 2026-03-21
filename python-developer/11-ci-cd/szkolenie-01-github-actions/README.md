# Szkolenie 1: CI/CD - GitHub Actions

Przykładowe workflow YAML z materiałów szkoleniowych dotyczących GitHub Actions.

## Pliki

- `.github/workflows/ci.yml` - Pipeline CI: linting (Ruff) + testy (pytest) z cache'owaniem zależności
- `.github/workflows/docker.yml` - Pipeline Docker: budowanie i pushowanie obrazu do GitHub Container Registry (GHCR)
- `.github/workflows/ci-cd.yml` - Kompletny pipeline CI/CD dla aplikacji Django: lint -> testy (matrix) z PostgreSQL -> budowanie obrazu Docker

## Użycie

Skopiuj pliki `.github/workflows/` do swojego repozytorium i dostosuj:

1. Wersję Pythona (`python-version`)
2. Zależności (`requirements.txt` lub Poetry)
3. Sekrety w ustawieniach repozytorium (Settings -> Secrets and variables -> Actions)

## Wymagania

- Repozytorium na GitHub
- Plik `requirements.txt` lub `pyproject.toml` w projekcie
- (Opcjonalnie) `Dockerfile` dla workflow Docker
