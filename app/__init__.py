from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
TMDB_ACCESS_TOKEN = os.getenv('TMDB_ACCESS_TOKEN', '')
GOOGLE_BOOKS_API_KEY = os.getenv('GOOGLE_BOOKS_API_KEY', '')
RAWG_API_KEY = os.getenv('RAWG_API_KEY', '')

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
            'rating': round(item.rating * 2) / 2 if item.rating is not None else None,
            'status': item.status,
            'notes': item.notes,
            'poster_path': item.poster_path,
            'external_id': item.external_id
        } for item in items])
    except Exception as e:
        app.logger.error(f'Error getting favorites: {str(e)}')
        return jsonify({'error': 'Could not fetch favorites'}), 500

@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    try:
        data = request.json
        app.logger.info(f'Attempting to add favorite: {data}')
        
        # Sprawdź czy element już istnieje
        existing_item = FavoriteItem.query.filter_by(
            external_id=str(data.get('external_id')),
            type=data.get('type')
        ).first()
        
        if existing_item:
            app.logger.info(f'Item already exists: {existing_item.id}')
            return jsonify({
                'error': 'Item already exists',
                'item': {
                    'id': existing_item.id,
                    'title': existing_item.title,
                    'type': existing_item.type,
                    'description': existing_item.description,
                    'external_id': existing_item.external_id,
                    'poster_path': existing_item.poster_path,
                    'rating': existing_item.rating,
                    'status': existing_item.status,
                    'notes': existing_item.notes
                }
            }), 409  # Conflict status code
        
        new_item = FavoriteItem(**data)
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({
            'id': new_item.id,
            'title': new_item.title,
            'type': new_item.type,
            'description': new_item.description,
            'external_id': new_item.external_id,
            'poster_path': new_item.poster_path,
            'rating': new_item.rating,
            'status': new_item.status,
            'notes': new_item.notes
        }), 201  # Created status code
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error adding favorite: {str(e)}')
        return jsonify({'error': 'Could not add favorite'}), 500

@app.route('/api/favorites/<int:item_id>', methods=['PUT'])
def update_favorite(item_id):
    try:
        data = request.json
        app.logger.info(f'Updating item {item_id} with data: {data}')  # Debug log
        
        item = FavoriteItem.query.get_or_404(item_id)
        
        # Aktualizacja wszystkich dozwolonych pól
        allowed_fields = ['title', 'type', 'description', 'external_id', 
                         'poster_path', 'status', 'rating', 'notes']
        
        for field in allowed_fields:
            if field in data:
                setattr(item, field, data[field])
            
        db.session.commit()
        
        return jsonify({
            'id': item.id,
            'title': item.title,
            'type': item.type,
            'description': item.description,
            'external_id': item.external_id,
            'poster_path': item.poster_path,
            'rating': item.rating,
            'status': item.status,
            'notes': item.notes
        })
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error updating favorite: {str(e)}')
        return jsonify({'error': 'Could not update favorite'}), 500

@app.route('/api/favorites/<int:item_id>', methods=['DELETE'])
def delete_favorite(item_id):
    try:
        item = FavoriteItem.query.get_or_404(item_id)
        db.session.delete(item)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error deleting favorite: {str(e)}')
        return jsonify({'error': 'Could not delete favorite'}), 500

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    search_type = request.args.get('type', 'all')
    results = []

    if search_type in ['all', 'movie']:
        # Wyszukiwanie filmów w TMDB
        try:
            tmdb_response = requests.get(
                'https://api.themoviedb.org/3/search/movie',
                params={'query': query, 'language': 'pl-PL'},
                headers={
                    'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}',
                    'accept': 'application/json'
                }
            )
            tmdb_data = tmdb_response.json()
            
            for movie in tmdb_data.get('results', []):
                results.append({
                    'id': str(movie['id']),
                    'title': movie['title'],
                    'type': 'movie',
                    'description': movie['overview'],
                    'poster_path': f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                    'rating': movie['vote_average']
                })
        except Exception as e:
            app.logger.error(f'TMDB API error: {str(e)}')

    if search_type in ['all', 'book'] and GOOGLE_BOOKS_API_KEY:
        # Wyszukiwanie książek w Google Books
        try:
            books_response = requests.get(
                'https://www.googleapis.com/books/v1/volumes',
                params={
                    'q': query,
                    'langRestrict': 'pl',
                    'key': GOOGLE_BOOKS_API_KEY
                }
            )
            books_data = books_response.json()
            
            for book in books_data.get('items', []):
                volume_info = book.get('volumeInfo', {})
                results.append({
                    'id': book['id'],
                    'title': volume_info.get('title', ''),
                    'type': 'book',
                    'description': volume_info.get('description', ''),
                    'poster_path': volume_info.get('imageLinks', {}).get('thumbnail'),
                    'rating': volume_info.get('averageRating', 0)
                })
        except Exception as e:
            app.logger.error(f'Google Books API error: {str(e)}')

    if search_type in ['all', 'game'] and RAWG_API_KEY:
        # Wyszukiwanie gier w RAWG
        try:
            games_response = requests.get(
                'https://api.rawg.io/api/games',
                params={
                    'search': query,
                    'key': RAWG_API_KEY
                }
            )
            games_data = games_response.json()
            
            for game in games_data.get('results', []):
                results.append({
                    'id': str(game['id']),
                    'title': game['name'],
                    'type': 'game',
                    'description': game.get('description', ''),
                    'poster_path': game.get('background_image'),
                    'rating': game.get('rating', 0)
                })
        except Exception as e:
            app.logger.error(f'RAWG API error: {str(e)}')

    return jsonify({'results': results}) 