#!/bin/bash

# Sprawdzenie czy istnieje środowisko wirtualne
if [ ! -d "venv" ]; then
    echo "Tworzenie środowiska wirtualnego..."
    python3 -m venv venv
    source venv/bin/activate
    pip install flask flask-cors flask-sqlalchemy python-dotenv requests
else
    echo "Aktywacja środowiska wirtualnego..."
    source venv/bin/activate
fi

# Przebudowanie frontendu Vue.js
echo "Przebudowanie frontendu Vue.js..."
cd frontend
npm install
npm run build
cd ..

# Uruchomienie aplikacji Flask
echo "Uruchamianie aplikacji..."
python3 run.py 