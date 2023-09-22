from app import app 

@app.route('/', methods=['GET'])
def index():
    return '<h1> This is Watamu API Application...</h1>'

