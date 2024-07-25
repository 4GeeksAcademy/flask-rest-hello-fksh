"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, Users, Characters, Planets, Favourites
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/users', methods=['GET'])
def list_user():
    users = Users.query.all()
    users_list = list(map(lambda users: users.serialize(), users))
    return jsonify(users_list), 200

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    users = Users.query.filter_by(id=user_id).first()
    if users is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(users.serialize()), 200

@app.route('/users', methods=['POST'])
def create_user():
    user_body = request.get_json()
    user_db = Users(
        first_name=user_body["first_name"],
        last_name=user_body["last_name"],
        email=user_body["email"],
        password=user_body["password"],
        is_active=user_body["is_active"]
    )
    db.session.add(user_db)
    db.session.commit()
    return jsonify(user_db.serialize()), 201

@app.route('/characters', methods=['GET'])
def list_characters():
    characters = Characters.query.all()
    characters_list = list(map(lambda characters: characters.serialize(), characters))
    return jsonify(characters_list), 200

@app.route('/characters/<int:character_id>', methods=['GET'])
def get_characters(character_id):
    characters = Characters.query.filter_by(id=character_id).first()
    if characters is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(characters.serialize()), 200

@app.route('/planets', methods=['GET'])
def list_planets():
    planets = Planets.query.all()
    planets_list = list(map(lambda item: item.serialize(), planets))
    return jsonify(planets_list), 200

@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets(planet_id):
    planets = Planets.query.filter_by(id=planet_id).first()
    if planets is None:
        return jsonify({"info": "Not found"}), 404
    return jsonify(planets.serialize()), 200
    
@app.route('/favourites', methods=['GET'])
def list_favourites():
    favourites = Favourites.query.all()
    favourites_list = list(map(lambda favourites: favourites.serialize(), favourites))
    return jsonify(favourites_list), 200

@app.route('/favourites/characters/<int:character_id>', methods=['POST'])
def add_character_favourite(character_id):
    character = Characters.query.filter_by(id=character_id).first()
    body_data = request.json
    user_id = body_data["user_id"]
    user = Users.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({"msg": "User doesn't exist"}), 404
    elif not character:
        return jsonify({"msg": "Character doesn't exist"}), 404

    existing_favourite = Favourites.query.filter_by(user_id=user_id, character_id=character_id).first()
    if existing_favourite:
        return jsonify({"msg": "Favourite already exists"}), 409

    new_favourite = Favourites(user_id=user_id, character_id=character_id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({"msg": "ok", "favourite": new_favourite.serialize()}), 201

@app.route('/favourites/planets/<int:planet_id>', methods=['POST'])
def add_planet_favourite(planet_id):
    planet = Planets.query.filter_by(id=planet_id).first()
    body_data = request.json
    user_id = body_data["user_id"]
    user = Users.query.filter_by(id=user_id).first()
    
    if not user:
        return jsonify({"msg": "User doesn't exist"}), 404
    elif not planet:
        return jsonify({"msg": "Planet doesn't exist"}), 404

    existing_favourite = Favourites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if existing_favourite:
        return jsonify({"msg": "Favourite already exists"}), 409

    new_favourite = Favourites(user_id=user_id, planet_id=planet_id)
    db.session.add(new_favourite)
    db.session.commit()
    return jsonify({"msg": "ok", "favourite": new_favourite.serialize()}), 201

@app.route('/favourites/characters/<int:character_id>', methods=['DELETE'])
def delete_favourite_character(character_id):
    body_data = request.json
    user_id = body_data.get("user_id")
    user = Users.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User doesn't exist"}), 404
    
    favourite = Favourites.query.filter_by(user_id=user_id, character_id=character_id).first()
    if not favourite:
        return jsonify({"msg": "Favourite character doesn't exist"}), 404
    
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({"msg": "Favourite character deleted"}), 200

@app.route('/favourites/planets/<int:planet_id>', methods=['DELETE'])
def delete_favourite_planet(planet_id):
    body_data = request.json
    user_id = body_data.get("user_id")
    user = Users.query.get(user_id)
    
    if not user:
        return jsonify({"msg": "User doesn't exist"}), 404
    
    favourite = Favourites.query.filter_by(user_id=user_id, planet_id=planet_id).first()
    if not favourite:
        return jsonify({"msg": "Favourite planet doesn't exist"}), 404
    
    db.session.delete(favourite)
    db.session.commit()
    return jsonify({"msg": "Favourite planet deleted"}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
