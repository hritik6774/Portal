
from flask import Flask
from flask_restful import Api
from resources.health import Health

app = Flask(__name__)
api = Api(app)

api.add_resource(Health, '/health')

if __name__ == "__main__":
    app.run(debug=True)