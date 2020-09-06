from flask_restful import Resource, reqparse

class Health(Resource):
    def get(self):
        return {'status': 'Healthy!'}, 200