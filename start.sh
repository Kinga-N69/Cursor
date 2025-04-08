#!/bin/bash

# Sprawdzenie czy istnieje środowisko wirtualne
if [ ! -d "venv" ]; then
    echo "Tworzenie środowiska wirtualnego..."
    python3 -m venv venv
    source venv/bin/activate
    pip install flask flask-cors flask-sqlalchemy python-dotenv
else
    echo "Aktywacja środowiska wirtualnego..."
    source venv/bin/activate
fi

# Uruchomienie aplikacji Flask
echo "Uruchamianie aplikacji..."
python3 run.py 