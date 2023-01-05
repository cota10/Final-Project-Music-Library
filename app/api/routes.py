from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Music, music_schema, musics_schema
from helpers import token_required

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/music', methods=['POST'])
@token_required
def create_music(current_user_token):
    artist_name = request.json['artist_name']
    fav_album = request.json['fav_album']
    fav_song_on_album = request.json['fav_song_on_album']
    user_token = current_user_token.token

    print(f'Big Test: {current_user_token.token}')

    music = Music(artist_name, fav_album, fav_song_on_album, user_token = user_token)

    db.session.add(music)
    db.session.commit()

    response = music_schema.dump(music)
    return jsonify(response)

@api.route('/music', methods=['GET'])
@token_required
def get_music(current_user_token):
    a_user = current_user_token.token
    musics = Music.query.filter_by(user_token=a_user).all()
    response = musics_schema.dump(musics)
    return jsonify(response)

@api.route('/music/<id>', methods = ['GET'])
@token_required
def get_single_music(current_user_token, id):
    music = Music.query.get(id)
    response = music_schema.dump(music)
    return jsonify(response)

@api.route('/music/<id>', methods = ['POST','PUT'])
@token_required
def update_music(current_user_token,id):
    music = Music.query.get(id) 
    music.artist_name = request.json['artist_name']
    music.fav_album = request.json['fav_album']
    music.fav_song_on_album = request.json['fav_song_on_album']
    music.user_token = current_user_token.token

    db.session.commit()
    response = music_schema.dump(music)
    return jsonify(response)

@api.route('/music/<id>', methods = ['DELETE'])
@token_required
def delete_music(current_user_token, id):
    music = Music.query.get(id)
    db.session.delete(music)
    db.session.commit()
    response = music_schema.dump(music)
    return jsonify(response)