from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# create flask application instance
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///watamu.db'

# third party package
db = SQLAlchemy() 

# called Once in manage.py
def create_app(): 
    CORS(app)

    CORS(app, origins="*")

    db.init_app(app)

    
    # add routes
    from app import routes

    return app

