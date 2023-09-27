from app import app, db
from flask import request, jsonify, make_response
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

from .models import Menu_item, Order, OrderItem, Restaurant, Menu, User

api = Api(app)
app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
jwt = JWTManager(app)


class UserRegistrationResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        parser.add_argument('phonenumber', type=str, required=False)
        args = parser.parse_args()

        # Check if the username or email already exists in the database
        if User.query.filter_by(username=args['username']).first() is not None:
            return {'message': 'Username already exists'}, 400
        if User.query.filter_by(email=args['email']).first() is not None:
            return {'message': 'Email already exists'}, 400

        # Create a new User instance and add it to the database
        new_user = User(
            username=args['username'],
            email=args['email'],
            password=args['password'],
            phonenumber=args['phonenumber']
        )
        db.session.add(new_user)
        db.session.commit()

        # Generate an access token for the newly registered user
        access_token = create_access_token(identity=new_user.id)

        return {
            'message': 'User registered successfully',
            'access_token': access_token
        }, 201
    
class UserLoginResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True)
        parser.add_argument('password', type=str, required=True)
        args = parser.parse_args()

        user = User.query.filter_by(username=args['username']).first()

        if user and user.password == args['password']:
            access_token = create_access_token(identity=user.id)
            return {'access_token': access_token}, 200
        else:
            return {'message': 'Invalid credentials'}, 401

class UserResource(Resource):
    @jwt_required()
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user.as_dict()

    @jwt_required()
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('email', type=str)
        parser.add_argument('phonenumber', type=int)
        args = parser.parse_args()

        for key, value in args.items():
            if value is not None:
                setattr(user, key, value)

        db.session.commit()
        return {'message': 'User updated successfully'}

    @jwt_required()
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {'message': 'User deleted successfully'}

class GetAllRestaurantResources(Resource):
    @jwt_required()
    def get(self):
        
        print(get_jwt_identity(), '-'*30)

        restaurants = Restaurant.query.all()
        rest = [rest.as_dict() for rest in restaurants]
        return rest
    
class RestaurantResource(Resource):
    @jwt_required()
    def get(self, restaurant_id):
        restaurant = Restaurant.query.get_or_404(restaurant_id)
        return restaurant.as_dict()

class MenuResource(Resource):
    @jwt_required()
    def get(self, restaurant_id):
        menu_items = Menu.query.filter_by(restaurant_id=restaurant_id).all()
        menu_data = [{'name': item.name, 'price': item.price, 'description': item.description} for item in menu_items]
        return menu_data

class OrderResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user_id', type=int, required=True)
        parser.add_argument('delivery_address_id', type=int, required=True)
        parser.add_argument('total', type=float, required=True)
        parser.add_argument('order_items', type=list, location='json', required=True)
        args = parser.parse_args()

        # Create a new Order instance and add it to the database
        new_order = Order(user_id=args['user_id'], delivery_address_id=args['delivery_address_id'], total=args['total'])
        db.session.add(new_order)

        # Process and add order items to the order
        for item_data in args['order_items']:
            menu_item_id = item_data['menu_item_id']
            quantity = item_data['quantity']
            menu_item = Menu_item.query.get_or_404(menu_item_id)
            order_item = OrderItem(menu_item_id=menu_item_id, quantity=quantity)
            new_order.orderitems.append(order_item)

        db.session.commit()
        return {'message': 'Order placed successfully'}, 201


api.add_resource(UserResource, '/user/<int:user_id>')
api.add_resource(GetAllRestaurantResources, '/restaurants')
api.add_resource(RestaurantResource, '/restaurant/<int:restaurant_id>')
api.add_resource(MenuResource, '/restaurant/<int:restaurant_id>/menu')
api.add_resource(OrderResource, '/order')
api.add_resource(UserLoginResource, '/login')
api.add_resource(UserRegistrationResource, '/register')
