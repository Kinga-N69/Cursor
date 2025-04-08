from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='../frontend/dist', static_url_path='')
CORS(app)

# Włączenie trybu debug
app.config['DEBUG'] = True

# Konfiguracja bazy danych
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///favorites.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Model danych
class FavoriteItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))  # movie, book, game
    description = db.Column(db.Text)
    external_id = db.Column(db.String(100))
    poster_path = db.Column(db.String(200))
    rating = db.Column(db.Float)
    status = db.Column(db.String(50))  # watching, completed, plan_to_watch
    notes = db.Column(db.Text)

# Tworzenie tabel i dodawanie przykładowych danych
with app.app_context():
    db.create_all()
    
    # Sprawdź czy są już jakieś dane
    if not FavoriteItem.query.first():
        # Dodaj przykładowe dane
        sample_items = [
            {
                'title': 'Wiedźmin 3: Dziki Gon',
                'type': 'game',
                'description': 'Gra RPG opowiadająca o przygodach Geralta z Rivii.',
                'poster_path': 'https://image.api.playstation.com/vulcan/ap/rnd/202211/0711/kh4MUIuMmHlktOHar3lVl6rY.png',
                'rating': 9.5,
                'status': 'completed',
                'notes': 'Jedna z najlepszych gier w jakie grałem!'
            },
            {
                'title': 'Władca Pierścieni: Drużyna Pierścienia',
                'type': 'book',
                'description': 'Pierwsza część epickiej trylogii J.R.R. Tolkiena.',
                'poster_path': 'https://ecsmedia.pl/c/wladca-pierscieni-druzyna-pierscienia-b-iext122973521.jpg',
                'rating': 9.0,
                'status': 'completed',
                'notes': 'Klasyka fantasy!'
            },
            {
                'title': 'Incepcja',
                'type': 'movie',
                'description': 'Film o złodzieju, który kradnie sekrety z podświadomości podczas snu.',
                'poster_path': 'https://fwcdn.pl/fpo/08/91/500891/7354571.3.jpg',
                'rating': 8.8,
                'status': 'completed',
                'notes': 'Świetny film, trzeba obejrzeć kilka razy'
            }
        ]
        
        for item in sample_items:
            new_item = FavoriteItem(**item)
            db.session.add(new_item)
        
        db.session.commit()

# Obsługa błędów
@app.errorhandler(404)
def not_found_error(error):
    if request.path.startswith('/api/'):
        return jsonify({'error': 'Not found'}), 404
    return send_from_directory(app.static_folder, 'index.html')

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

# Routing
@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def static_proxy(path):
    try:
        # Najpierw próbujemy znaleźć plik statyczny
        return send_from_directory(app.static_folder, path)
    except:
        # Jeśli nie znaleziono pliku, zwracamy index.html dla obsługi Vue Router
        return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/favorites', methods=['GET'])
def get_favorites():
    try:
        items = FavoriteItem.query.all()
        return jsonify([{
            'id': item.id,
            'title': item.title,
            'type': item.type,
            'description': item.description,
            'rating': item.rating,
            'status': item.status,
            'notes': item.notes,
            'poster_path': item.poster_path
        } for item in items])
    except Exception as e:
        app.logger.error(f'Error getting favorites: {str(e)}')
        return jsonify({'error': 'Could not fetch favorites'}), 500

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    try:
        data = request.json
        new_item = FavoriteItem(**data)
        db.session.add(new_item)
        db.session.commit()
        return jsonify({
            'id': new_item.id,
            'title': new_item.title,
            'type': new_item.type,
            'description': new_item.description,
            'rating': new_item.rating,
            'status': new_item.status,
            'notes': new_item.notes,
            'poster_path': new_item.poster_path
        })
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding favorite: {str(e)}')
        return jsonify({'error': 'Could not add favorite'}), 500 