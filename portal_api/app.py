
from flask import Flask
from flask_restful import Api
from resources.health import Health

app = Flask(__name__)
api = Api(app)


@app.route("/")
def placeholder():
    return 'Coming soon...'


api.add_resource(Health, '/health')

if __name__ == "__main__":
    app.run(port=8080, host='0.0.0.0', debug=True)
