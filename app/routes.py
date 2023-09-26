from app import app, db
from flask import request, jsonify, make_response
from flask_restful import Resource, Api, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from .models import Restaurant, User

# initialize API
api = Api(app)
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'wertyui'

class UserRegisterResource(Resource):
    def post(self):
         
        #  get data from reqyest

        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        phonenumber = data.get('phonenumber')

        # check if user exists in db

        new_user = User(
             username=username,
             email=email,
             password=password,
             phonenumber=phonenumber
        )

        db.session.add(new_user)
        db.session.commit()

        # generate access token for user
        access_token = create_access_token(identity=new_user.id)

        return {
             'message':'User created',
             'access_token': access_token
        }, 201

api.add_resource(UserRegisterResource, '/register')

class UserLoginResource(Resource):
    def post(self):
         
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # get user from database
        user = User.query.filter_by(username=username).first()
        print(user, '*'*50)
        if user is None:
            return {'message':'User not found'}, 404

        # check if password is correct

        # generate access token for user
        access_token = create_access_token(identity=user.id)

        return {
            'message':'login successful',
            'access_token':access_token
        }


api.add_resource(UserLoginResource, '/login')
                 
class IndexResource(Resource):
    def get(self):
        return {"result":"This is Watamu API Application..."}, 200

api.add_resource(IndexResource, '/')

class GetAllRestaurantsResource(Resource):
    @jwt_required()
    def get(self):
        restaurant = Restaurant.query.all()

        rest = [rest.as_dict() for rest in restaurant]

        return {'result': rest}, 200
    
    def post(self):
            data = request.get_json()

            # create a new restaurant
            newrestaurant = Restaurant(**data)

            # save data
            db.session.add(newrestaurant)
            db.session.commit()

            return {'message': 'Added Successfully'}, 201

api.add_resource(GetAllRestaurantsResource, '/restaurants')


# @app.route('/', methods=['GET'])
# def index():
#     return jsonify({"message":"This is Watamu API Application..."}), 200


# @app.route('/restaurants', methods=['GET'])
# def get_restaurants():
#     restaurants = Restaurant.query.all()
#     rest  = []

#     for restaurant in restaurants:
#         rest.append(restaurant.as_dict())
        
#     return jsonify({"message": rest})

# @app.route('/add_restaurant', methods=['POST'])
# def add_restaurant():
#     data = request.get_json()

#     # create a new restaurant
#     newrestaurant = Restaurant(**data)

#     # save data
#     db.session.add(newrestaurant)
#     db.session.commit()

#     return jsonify({'message': 'Add Successfully'}), 201