from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import requests

load_dotenv()

TMDB_API_KEY = os.getenv('TMDB_API_KEY', '')
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
    try:
        query = request.args.get('query', '')
        search_type = request.args.get('type', 'all')  # all, movie, book, game
        results = []

        # Wyszukiwanie filmów przez TMDB API
        if search_type in ['all', 'movie']:
            tmdb_url = f'https://api.themoviedb.org/3/search/movie'
            response = requests.get(tmdb_url, params={
                'api_key': TMDB_API_KEY,
                'query': query,
                'language': 'pl-PL'
            })
            if response.status_code == 200:
                for item in response.json().get('results', [])[:5]:
                    results.append({
                        'id': f"movie_{item['id']}",
                        'title': item['title'],
                        'type': 'movie',
                        'description': item['overview'],
                        'poster_path': f"https://image.tmdb.org/t/p/w500{item['poster_path']}" if item.get('poster_path') else None,
                        'rating': item['vote_average']
                    })

        # Wyszukiwanie książek przez Google Books API
        if search_type in ['all', 'book']:
            books_url = 'https://www.googleapis.com/books/v1/volumes'
            response = requests.get(books_url, params={
                'q': query,
                'key': GOOGLE_BOOKS_API_KEY,
                'langRestrict': 'pl',
                'maxResults': 5
            })
            if response.status_code == 200:
                for item in response.json().get('items', []):
                    volume_info = item.get('volumeInfo', {})
                    results.append({
                        'id': f"book_{item['id']}",
                        'title': volume_info.get('title', ''),
                        'type': 'book',
                        'description': volume_info.get('description', ''),
                        'poster_path': volume_info.get('imageLinks', {}).get('thumbnail'),
                        'rating': volume_info.get('averageRating', 0)
                    })

        # Wyszukiwanie gier przez RAWG API
        if search_type in ['all', 'game']:
            rawg_url = 'https://api.rawg.io/api/games'
            response = requests.get(rawg_url, params={
                'key': RAWG_API_KEY,
                'search': query,
                'page_size': 5
            })
            if response.status_code == 200:
                for item in response.json().get('results', []):
                    results.append({
                        'id': f"game_{item['id']}",
                        'title': item['name'],
                        'type': 'game',
                        'description': item.get('description', ''),
                        'poster_path': item.get('background_image'),
                        'rating': item.get('rating', 0)
                    })

        return jsonify({'results': results})
    except Exception as e:
        app.logger.error(f'Error searching: {str(e)}')
        return jsonify({'error': 'Could not perform search'}), 500 