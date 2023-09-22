from flask_sqlalchemy import SQLalchemy

db = SQLalchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phonenumber = db.Column(db.Integer, nullable=True)

    addresses = db.relationship('User_address', backref='user', lazy='True')
    order = db.relationship('Order', backref='user', lazy='True')


class User_address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    location_address = db.Column(db.String(1000), nullable=False)
    street_name = db.Column(db.String(60), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    county = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    order = db.relationship('Order', backref='userAddress', lazy=True)
######################### Restaurant ###########################

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=False)

    menus = db.relationship('Menu', backref='restaurant', lazy='True')

class Menu(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=True)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurant.id', nullable=False))

    menu_items = db.relationship('Menu_item', backref='menu', lazy='True')

class Menu_item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu.id'), nullable=False)

    orderitem = db.relationship('OrderItem', backref='menu_item', lazy='True')


######################### Order ###########################

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    delivery_address_id = db.Column(db.Integer, db.ForeignKey('userAddress.id'), nullable=False)
    total = db.Column(db.Float, nullable=False)

    orderitems = db.relationship('OrderItem', backref='order', lazy=True)

class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    menu_item_id = db.Column(db.Integer, db.ForeignKey('menu_item.id'), nullable=False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    quantity = db.Column(db.Integer, default=1, nullable=False)
