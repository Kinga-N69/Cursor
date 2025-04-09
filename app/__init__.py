from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import requests
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
from functools import wraps
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token
import logging

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
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///favorites.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'your-secret-key')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)
db = SQLAlchemy(app)
jwt = JWTManager(app)

# Konfiguracja logowania
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    favorites = db.relationship('Favorite', backref='user', lazy=True)

    def set_password(self, password):
        self.password = password

    def check_password(self, password):
        return self.password == password

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    external_id = db.Column(db.String(100))
    poster_path = db.Column(db.String(500))
    status = db.Column(db.String(50), default='plan_to_watch')
    rating = db.Column(db.Float)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

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
@jwt_required()
def get_favorites():
    current_user_id = get_jwt_identity()
    favorites = Favorite.query.filter_by(user_id=current_user_id).all()
    return jsonify([{
        'id': f.id,
        'title': f.title,
        'type': f.type,
        'description': f.description,
        'external_id': f.external_id,
        'poster_path': f.poster_path,
        'status': f.status,
        'rating': f.rating,
        'notes': f.notes,
        'created_at': f.created_at.isoformat(),
        'updated_at': f.updated_at.isoformat()
    } for f in favorites])

@app.route('/api/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    if not data or not data.get('title') or not data.get('type'):
        return jsonify({'error': 'Missing required fields'}), 400
        
    favorite = Favorite(
        user_id=current_user_id,
        title=data['title'],
        type=data['type'],
        description=data.get('description'),
        external_id=data.get('external_id'),
        poster_path=data.get('poster_path'),
        status=data.get('status', 'plan_to_watch'),
        rating=data.get('rating'),
        notes=data.get('notes')
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify({
        'id': favorite.id,
        'title': favorite.title,
        'type': favorite.type,
        'description': favorite.description,
        'external_id': favorite.external_id,
        'poster_path': favorite.poster_path,
        'status': favorite.status,
        'rating': favorite.rating,
        'notes': favorite.notes,
        'created_at': favorite.created_at.isoformat(),
        'updated_at': favorite.updated_at.isoformat()
    }), 201

@app.route('/api/favorites/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_favorite(item_id):
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    favorite = Favorite.query.filter_by(id=item_id, user_id=current_user_id).first()
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
        
    logger.info(f"Updating favorite {item_id} with data: {data}")
    
    allowed_fields = ['title', 'type', 'description', 'external_id', 'poster_path', 'status', 'rating', 'notes']
    for field in allowed_fields:
        if field in data:
            setattr(favorite, field, data[field])
            
    try:
        db.session.commit()
        return jsonify({
            'id': favorite.id,
            'title': favorite.title,
            'type': favorite.type,
            'description': favorite.description,
            'external_id': favorite.external_id,
            'poster_path': favorite.poster_path,
            'status': favorite.status,
            'rating': favorite.rating,
            'notes': favorite.notes,
            'created_at': favorite.created_at.isoformat(),
            'updated_at': favorite.updated_at.isoformat()
        })
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating favorite {item_id}: {str(e)}")
        return jsonify({'error': 'Failed to update favorite'}), 500

@app.route('/api/favorites/<int:item_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(item_id):
    current_user_id = get_jwt_identity()
    
    favorite = Favorite.query.filter_by(id=item_id, user_id=current_user_id).first()
    if not favorite:
        return jsonify({'error': 'Favorite not found'}), 404
        
    try:
        db.session.delete(favorite)
        db.session.commit()
        return '', 204
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting favorite {item_id}: {str(e)}")
        return jsonify({'error': 'Failed to delete favorite'}), 500

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
                params={
                    'query': query, 
                    'language': 'pl-PL',
                    'sort_by': 'popularity.desc'
                },
                headers={
                    'Authorization': f'Bearer {TMDB_ACCESS_TOKEN}',
                    'accept': 'application/json'
                }
            )
            tmdb_data = tmdb_response.json()
            
            # Sortuj wyniki według popularności
            movies = sorted(
                tmdb_data.get('results', []),
                key=lambda x: (x.get('popularity', 0), x.get('vote_average', 0)),
                reverse=True
            )
            
            for movie in movies:
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

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
        
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'Username already exists'}), 400
        
    user = User(username=data['username'], password=data['password'])
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({'error': 'Missing username or password'}), 400
        
    user = User.query.filter_by(username=data['username']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid username or password'}), 401
        
    access_token = create_access_token(identity=user.id)
    return jsonify({'token': access_token}), 200

@app.route('/api/auth/me', methods=['GET'])
@jwt_required()
def get_current_user():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    return jsonify({
        'id': user.id,
        'username': user.username
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001) 