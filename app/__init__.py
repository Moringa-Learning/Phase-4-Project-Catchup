from flask import Flask

app = Flask(__name__)

def create_app(): # called Once in manage.py

    # add routes
    from app import routes

    return app

