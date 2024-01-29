#!/usr/bin/env python3

from flask import Flask, make_response,jsonify,request
from flask_migrate import Migrate

from models import db, Hero,Power,HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrate = Migrate(app,db)

db.init_app(app)

@app.route('/')
def home():
    return ''


@app.route('/heroes',methods=['GET'])
def get_heroes():
        heroes=Hero.query.all()
        heroes_data=[
            {"id":hero.id,"name":hero.name,"super_name":hero.super_name}
             for hero in heroes
        ]

        response=make_response(
             jsonify(heroes_data),
             200
        )
        return response

@app.route('/heroes/:id',methods=['GET'])
def  get_heroes_by_id(id):
    hero=Hero.query.filter_by(id=id).first()

    if request.method=='GET':
        hero_dict=hero.to_dict()

        response=make_response(
              jsonify(hero_dict),
              200
        )
        return response

    if hero is None:
        response=make_response( {"error":"Hero not found"},404
        )
        return response
    
@app.route('/powers',methods=['GET'])
def get_powers():
    powers=Power.query.all()
    powers_data=[
        {"id":power.id,
         "name":power.name,
         "description":power.description}
        for power in powers
    ]

    response=make_response(
        jsonify(powers_data),
        200
    )
    return response

@app.route('/powers/:id',methods=['GET','PATCH'])
def  get_patch_powers_by_id(id):
    power=Power.query.filter_by(id=id).first()

    if request.method=='GET':
        power_dict=power.to_dict()

        response=make_response(
              jsonify(power_dict),
              200
        )
        return response
    
    if request.method =='PATCH':
        for attr in request.form:
            setattr(power,attr,request.form.get(attr))

        db.session.add(power)
        db.session.commit()

        power_dict=power.to_dict()

        response=make_response(
            jsonify(power_dict),
            200
        )
        return response
    
@app.route('/heropowers',methods=['POST'])
def post_heropowers():
    if request.method=='POST':
        new_heropower=HeroPower(
            hero_id=request.form.get('hero_id'),
            power_id=request.form.get('power_id'),
            strength=request.form.get('strength'),
        )
        db.session.add(new_heropower)
        db.session.commit()

        heropower_dict=new_heropower.to_dict()

        response=make_response(
            jsonify(heropower_dict),
            201
        ) 
        return response


     

if __name__ == '__main__':
    app.run(port=4000)
