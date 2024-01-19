from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
class Planet(db.Model):
    __tablename__ = 'planet'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    terrain = db.Column(db.String(80), unique=False, nullable=False)
    diameter = db.Column(db.Integer, unique=False, nullable=False)

    def __repr__(self):
        return f"planet {self.name} with ID {self.id}" 
    
    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "terrain": self.terrain,
            "diameter": self.diameter
        }
    
class Character(db.Model):
    __tablename__ = 'character'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    hair_color = db.Column(db.String(50), unique=False, nullable=False)
    eye_color = db.Column(db.String(50), unique=False, nullable=False)
    
    def __rep__(self):
        return f"characters {self.name} with ID {self.id}"
    
    def serialize(self):
        return {
            "id" : self.id,
            "name": self.name,
            "hair color": self.hair_color,
            "eye color": self.eye_color
        }
    
class FavouritePlanet(db.Model):
    __tablename__='favouritePlanet'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"))
        
    def __repr__(self):
        return '<favouritePlanets %r>' % self.id
        
    def serialize(self):
        return {
            "planets": self.planets.serialize(),
        }
    
class FavouriteCharacter(db.Model):
    __tablename__='favouriteCharacter'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
       
    def __repr__(self):
        return '<favouriteCharacters %r>' % self.id
        
    def serialize(self):
        return {
            "characters": self.characters.serialize(),
        }