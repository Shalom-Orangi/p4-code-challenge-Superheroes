from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    super_name=db.Column(db.String)

    heropowers=db.relationship('HeroPower',back_populates='hero')
    
    def __repr__(self):
        return f"<{self.name},{self.super_name}>"
    

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String)
    description=db.Column(db.String)

    heropowers=db.relationship('HeroPower',back_populates='power')

    @validates('description')
    def validate_description(self,key,description):
        if len(description)<20:
            raise ValueError("Description must be atleast 20 characters")
        return description
    
    def __repr__(self):
        return f'<{self.name},{self.description}>'


class HeroPower(db.Model):
    __tablename__ = 'heropowers'

    id = db.Column(db.Integer, primary_key=True)
    hero_id=db.Column(db.Integer,db.ForeignKey("heroes.id"),nullable=False)
    power_id=db.Column(db.Integer, db.ForeignKey("powers.id"),nullable=False)
    strength=db.Column(db.String)

    hero=db.relationship('Hero',back_populates='heropowers')
    power=db.relationship('Power',back_populates='heropowers')

    @validates('strength')
    def validate_strength(self,key,strength):
        valid_strengths=['Strong','Weak','Average']
        if strength not in valid_strengths:
            raise ValueError("Strength ranges from:'Strong','Weak','Average'")
        return strength
    
    def __repr__(self) :
        return f"<{self.hero_id},{self.power_id},{self.strength}>"
