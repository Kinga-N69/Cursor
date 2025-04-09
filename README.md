# Favorite Tracker

Aplikacja do śledzenia ulubionych filmów, książek i gier. Pozwala na wyszukiwanie treści, dodawanie ich do ulubionych, zarządzanie statusem, ocenami i notatkami.

## Funkcjonalności

- **Wyszukiwanie** - wyszukiwanie filmów, książek i gier za pomocą API TMDb
- **Autentykacja** - rejestracja i logowanie użytkowników
- **Ulubione** - dodawanie, usuwanie i zarządzanie ulubionymi pozycjami
- **Status** - oznaczanie statusu (do obejrzenia, w trakcie, obejrzane)
- **Oceny** - dodawanie ocen do ulubionych pozycji
- **Notatki** - dodawanie notatek do ulubionych pozycji
- **Responsywny design** - aplikacja działa poprawnie na urządzeniach mobilnych i desktopowych

## Wymagania

- Python 3.8+
- Node.js 14+
- npm 6+
- Klucz API z TMDb (https://www.themoviedb.org/settings/api)

## Instalacja

1. Sklonuj repozytorium:
```bash
git clone <repository-url>
cd favorite-tracker
```

2. Zainstaluj zależności Pythona:
```bash
pip install -r requirements.txt
```

3. Zainstaluj zależności Vue.js:
```bash
cd frontend
npm install
```

4. Skonfiguruj zmienne środowiskowe:
- Skopiuj plik `.env.example` do `.env` (lub utwórz plik `.env`)
- Uzupełnij `TMDB_API_KEY` swoim kluczem API z TMDb
- Opcjonalnie ustaw `PORT` (domyślnie 5001)

## Uruchomienie w trybie developerskim

1. Uruchom backend Flask:
```bash
python run.py
```

2. W osobnym terminalu uruchom frontend Vue:
```bash
cd frontend
npm run dev
```

## Budowanie do produkcji

1. Zbuduj frontend:
```bash
cd frontend
npm run build
```

2. Uruchom aplikację:
```bash
python run.py
```

Alternatywnie, możesz użyć skryptu start.sh:
```bash
chmod +x start.sh
./start.sh
```

Aplikacja będzie dostępna pod adresem http://localhost:5001 (lub innym portem, jeśli został zmieniony w pliku .env)

## Struktura projektu

- `app/` - backend Flask
  - `__init__.py` - główny plik aplikacji Flask
  - `routes.py` - dodatkowe trasy API
- `frontend/` - frontend Vue.js
  - `src/` - kod źródłowy Vue.js
    - `views/` - komponenty widoków (HomeView, LoginView, RegisterView, FavoritesView)
    - `stores/` - magazyny Pinia (auth, favorites)
    - `router/` - konfiguracja routera Vue
    - `components/` - komponenty wielokrotnego użytku
    - `assets/` - zasoby statyczne
- `run.py` - skrypt uruchamiający aplikację Flask
- `start.sh` - skrypt do uruchamiania aplikacji w środowisku produkcyjnym
- `requirements.txt` - zależności Pythona
- `.env` - zmienne środowiskowe

## Technologie

- **Backend**: Flask, SQLAlchemy, JWT
- **Frontend**: Vue.js 3, Pinia, Vue Router
- **API**: TMDb API
- **Baza danych**: SQLite (domyślnie) 