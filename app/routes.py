from app import app, db
from flask import request, jsonify, make_response

from .models import Restaurant

@app.route('/', methods=['GET'])
def index():
    data = jsonify({"message":"This is Watamu API Application..."})
    return data

@app.route('/restaurants', methods=['GET'])
def get_restaurants():
    restaurants = Restaurant.query.all()
    rest  = []

    for restaurant in restaurants:
        rest.append(restaurant.as_dict())
        
    return jsonify({"message": rest})

@app.route('/add_restaurant', methods=['POST'])
def add_restaurant():
    data = request.get_json()

    # create a new restaurant
    newrestaurant = Restaurant(**data)

    # save data
    db.session.add(newrestaurant)
    db.session.commit()

    return jsonify({'message': 'Add Successfully'}), 201