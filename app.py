from flask import Flask
from flask_restful import Api
from os import environ
from dotenv import load_dotenv
from routes import init_routes
from models.share import db

# Load environment variables
load_dotenv()

# Initialize the app
app = Flask(__name__)
api = Api(app,prefix="/api/"+environ.get('API_VERSION'))

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('MYSQL_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

# Routes
init_routes(api)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5001)

