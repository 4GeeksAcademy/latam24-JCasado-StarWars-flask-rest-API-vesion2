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
from models import db, User, Planet, Character

#Handle/serialize errors like a JSON object

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")

if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("posgres://", "posgresql://")

else: 
    app.config['SQLALCHEMY_DATABASE_URL'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.errorhandler(APIException)
def handle_invalid_usage(error):

    return jsonify(error.to_dict()), error.status_code
 
@app.route('/user', methods= ['GET'])
def handle_hello():

    response_body = {
        "msg": "Hi this is your GET /user response"
    }

    return jsonify(response_body), 200


@app.route("/planet", methods= ['GET'])
def get_all_planets():
    planet = Planet.query.all()
    planet_serialized = list(map(lambda x: x.serialize(), planet))

    return jsonify({"msg": "Completed", "planets": planet_serialized})

@app.route('/planet/<int:planet_id>', methods=['GET'])
def handle_planet(planet_id):
    single_planet = Planet.query.get(planet_id)

    if single_planet is None:
       raise APIException(f"Planet ID not found {planet_id}", status_code=400)
    
    response_body = {
        "msg": "Hello, this is your GET /planets response",
        "planets_id": planet_id,
        "planets_info": single_planet.serialize()
    }

    return jsonify(response_body), 200

@app.route("/characters", methods= ['GET'])
def get_all_characters():
    character = Character.query.all()
    characters_serialized = list(map(lambda x: x.serialize(), character))
    return jsonify({"msg": "Completed", "Characters": characters_serialized})

@app.route('/characters/<int:character_id>', methods=['GET'])
def handle_character(character_id):
    single_character = Character.query.get(character_id)

    if single_character is None:
       raise APIException(f"Character ID not found {character_id}", status_code=400)
    
    response_body = {
        "msg": "Hello, this is your GET /characters response",
        "planets_id": character_id,
        "planets_info": single_character.serialize()
    }

    return jsonify(response_body), 200


@app.route("/user", methods= ['GET'])
def get_all_users():
    user = User.query.all()
    users_serialized = list(map(lambda x: x.serialize(), user))

    return jsonify({"msg": "Completed", "users": users_serialized})


@app.route('/user/<int:user_id>', methods=['GET'])

def handle_users(user_id):
    single_user = User.query.get(user_id)

    if single_user is None:
       raise APIException(f"User ID not found {user_id}", status_code=400)
    
    response_body = {
        "msg": "Hello, this is your GET /users response ",
        "user_id": user_id,
        "user_info": single_user.serialize()
    }

    return jsonify(response_body), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
