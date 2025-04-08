from flask import Blueprint, jsonify, request
from sqlalchemy.orm import Session
from . import models, database
import requests
import os
from dotenv import load_dotenv

load_dotenv()

api = Blueprint('api', __name__)
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
TMDB_BASE_URL = "https://api.themoviedb.org/3"

@api.route('/api/search', methods=['GET'])
def search_movies():
    query = request.args.get('query', '')
    if not query:
        return jsonify({'results': []})
    
    response = requests.get(
        f"{TMDB_BASE_URL}/search/movie",
        params={
            'api_key': TMDB_API_KEY,
            'query': query,
            'language': 'pl-PL'
        }
    )
    return jsonify(response.json())

@api.route('/api/favorites', methods=['GET'])
def get_favorites():
    db = next(database.get_db())
    items = db.query(models.FavoriteItem).all()
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

@api.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.json
    db = next(database.get_db())
    new_item = models.FavoriteItem(
        title=data['title'],
        type=data['type'],
        description=data.get('description', ''),
        external_id=data.get('external_id', ''),
        poster_path=data.get('poster_path', ''),
        rating=data.get('rating', 0),
        status=data.get('status', 'plan_to_watch'),
        notes=data.get('notes', '')
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return jsonify({'id': new_item.id}) 