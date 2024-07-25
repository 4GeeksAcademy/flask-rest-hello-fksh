from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120), unique=False, nullable=False)
    last_name = db.Column(db.String(120), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<Users %r>' % self.first_name

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Characters(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    characters_name = db.Column(db.String(120), unique=False, nullable=False)
    hair_colour = db.Column(db.String(120), unique=False, nullable=False)
    skin_colour = db.Column(db.String(120), unique=False, nullable=False)
    eye_colour = db.Column(db.String(120), unique=False, nullable=False)
    birth_year = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return '<Characters %r>' % self.characters_name
        
    def serialize(self):
        return {
            "id": self.id,
            "characters_name": self.characters_name,
            "hair_colour": self.hair_colour,
            "skin_colour": self.skin_colour,
            "eye_colour": self.eye_colour,
            "birth_year": self.birth_year,
        }


class Planets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    planets_name = db.Column(db.String(120), unique=False, nullable=False)
    climate = db.Column(db.String(120), unique=False, nullable=False)
    terrain = db.Column(db.String(120), unique=False, nullable=False)
    population = db.Column(db.Integer, unique=False, nullable=False)
    gravity = db.Column(db.Float, unique=False, nullable=False)

    def __repr__(self):
        return '<Planets %r>' % self.planets_name

    def serialize(self):
            return {
            "id": self.id,
            "planets_name": self.planets_name,
            "climate": self.climate,
            "terrain": self.climate,
            "population": self.population,
            "gravity": self.population,
        }
    
class Favourites(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    character_id = db.Column(db.Integer, db.ForeignKey('characters.id'), nullable=True)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'), nullable=True)

    def __repr__(self):
        return '<Favourites %r>' % self.id

    def serialize(self):
        character = Characters.query.filter_by(id=self.character_id).first()
        planet = Planets.query.filter_by(id=self.planet_id).first()

        if self.character_id is not None:
            return {
                "id": self.id,
                "user_id": self.user_id,
                "character_id": self.character_id,
                "character_name": character.serialize() if character else None,
            }
        elif self.planet_id is not None:
            return {
                "id": self.id,
                "user_id": self.user_id,
                "planet_id": self.planet_id,
                "planet_info": planet.serialize() if planet else None,
            }

    @property
    def character_name(self):
        character = Characters.query.filter_by(id=self.character_id).first()
        return character.characters_name if character else "N/A"

    @property
    def planet_name(self):
        planet = Planets.query.filter_by(id=self.planet_id).first()
        return planet.planets_name if planet else "N/A"
