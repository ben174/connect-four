from flask import Flask, request
from flask_restful import reqparse, Resource, Api
from werkzeug.exceptions import BadRequest

from evaluator import ConnectFourEvaluator


app = Flask(__name__)
api = Api(app)


class ConnectFourEndpoint(Resource):
    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('board', type=list, location='json')

    def post(self):
        args = self.parser.parse_args()
        if not args['board']:
            e = BadRequest('Please provide a json object with a board')
            raise e

        evaluator = ConnectFourEvaluator(args['board'])
        evaluator.evaluate()
        print(evaluator.response)
        if evaluator.response['error']:
            e = BadRequest(evaluator.response['error'])
            e.data = evaluator.response
            raise e
        return evaluator.response

api.add_resource(ConnectFourEndpoint, '/evaluate_board_state')

if __name__ == '__main__':
    app.run(debug=True, port=8081)
