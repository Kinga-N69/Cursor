# Favorite Tracker

Aplikacja do śledzenia ulubionych filmów, książek i gier.

## Wymagania

- Python 3.8+
- Node.js 14+
- npm 6+

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
- Skopiuj plik `.env.example` do `.env`
- Uzupełnij `TMDB_API_KEY` swoim kluczem API z TMDb

## Uruchomienie w trybie developerskim

1. Uruchom backend Flask:
```bash
python app.py
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
python app.py
```

Aplikacja będzie dostępna pod adresem http://localhost:5000 