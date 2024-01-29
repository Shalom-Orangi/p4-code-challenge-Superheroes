from random import randint, choice
from faker import Faker
from app import app
from models import db, Hero, Power, HeroPower

fake = Faker()

with app.app_context():

    Hero.query.delete()
    Power.query.delete()
    HeroPower.query.delete()

    # Seed powers
    powers_data = [
        {"name": "super strength", "description": "gives the wielder super-human strengths"},
        {"name": "flight", "description": "gives the wielder the ability to fly through the skies at supersonic speed"},
        {"name": "super human senses", "description": "allows the wielder to use her senses at a super-human level"},
        {"name": "elasticity", "description": "can stretch the human body to extreme lengths"}
    ]

    powers = []
    for power_info in powers_data:
        power = Power(**power_info)
        powers.append(power)

    db.session.add_all(powers)
    db.session.commit()

    # Seed heroes
    heroes_data = [
        {"name": "Kamala Khan", "super_name": "Ms. Marvel"},
        {"name": "Doreen Green", "super_name": "Squirrel Girl"},
        {"name": "Gwen Stacy", "super_name": "Spider-Gwen"},
        {"name": "Janet Van Dyne", "super_name": "The Wasp"},
        {"name": "Wanda Maximoff", "super_name": "Scarlet Witch"},
        {"name": "Carol Danvers", "super_name": "Captain Marvel"},
        {"name": "Jean Grey", "super_name": "Dark Phoenix"},
        {"name": "Ororo Munroe", "super_name": "Storm"},
        {"name": "Kitty Pryde", "super_name": "Shadowcat"},
        {"name": "Elektra Natchios", "super_name": "Elektra"}
    ]

    heroes = []
    for hero_info in heroes_data:
        hero = Hero(**hero_info)
        heroes.append(hero)

    db.session.add_all(heroes)
    db.session.commit()

    # Seed hero powers
    strengths = ["Strong", "Weak", "Average"]

    for hero in Hero.query.all():
        for _ in range(randint(1, 3)):
            power = Power.query.order_by(db.func.random()).first()
            hero_power = HeroPower(hero_id=hero.id, power_id=power.id, strength=choice(strengths))
            db.session.add(hero_power)

    db.session.commit()