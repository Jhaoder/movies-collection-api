from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movies.db'
db = SQLAlchemy(app)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    title = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/api/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    movies_json = []

    for movie in movies: 
        movies_json.append({'id': movie.id, 
        'title': movie.title, 'genre': movie.genre})
        
    return jsonify(movies_json)

@app.route('/api/movie/<int:id>', methods=['GET'])
def get_movie(id):
    movie = Movie.query.get(id)

    return jsonify({'id': movie.id, 
        'title': movie.title, 'genre': movie.genre}) if movie else ('', 404)

@app.route('/api/movies/', methods=['POST'])
def add_movie():
    data = request.get_json()
    new_movie = Movie(title=data['title'], genre=data['genre'])
    db.session.add(new_movie)
    db.session.commit()

    return jsonify({'id': new_movie.id, 
        'title': new_movie.title, 'genre': new_movie.genre}), 201

@app.route('/api/movies/<int:id>', methods=['DELETE'])
def delete_movie(id):
    movie = Movie.query.get(id)
    if movie is None:
            return jsonify({'error': 'Movie not found'}), 404
    
    db.session.delete(movie)
    db.session.commit()
    return '', 204
            
@app.route('/api/movies/<int:id>', methods=['PUT'])
def update_movie(id):
    movie = Movie.query.get(id)

    if movie is None: 
        return jsonify({'error': 'Movie not found'}), 404
    
    data = request.get_json()
    movie.title = data.get('title', movie.title)
    movie.genre = data.get('genre', movie.genre)
    db.session.commit()
    
    return jsonify({'id': movie.id, 
        'title': movie.title, 'genre': movie.genre}), 201
    
if __name__ == '__main__':
    app.run(port=5000, debug=True)