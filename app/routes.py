@app.route('/api/favorites', methods=['POST'])
def add_favorite():
    data = request.get_json()
    
    # Sprawdź czy element już istnieje
    existing = Favorite.query.filter_by(
        external_id=str(data['external_id']),
        type=data['type']
    ).first()
    
    if existing:
        app.logger.info(f"Item already exists: {data}")
        return jsonify(existing.to_dict()), 200
        
    app.logger.info(f"Adding new favorite: {data}")
    favorite = Favorite(
        title=data['title'],
        external_id=str(data['external_id']),
        type=data['type'],
        image_url=data.get('image_url', ''),
        rating=data.get('rating', None),
        note=data.get('note', '')
    )
    
    db.session.add(favorite)
    db.session.commit()
    
    return jsonify(favorite.to_dict()), 201 