from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

pokedex = [{'number': 14, 'name': 'Kakuna'},
           {'number': 16, 'name': 'Pidgey'},
           {'number': 50, 'name': 'Diglett'}]


class Pokemon(Resource):
    def get(self):
        return pokedex

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, location='json')
        parser.add_argument('number', type=int, location='json')

        args = parser.parse_args(strict=True)
        name = args['name']
        number = args['number']
        pokemon = {'name': name, 'number': number}
        if pokemon in pokedex or name is None or number is None:
            return {}

        pokedex.append(pokemon)
        return pokedex[-1]

api.add_resource(Pokemon, '/api/v1/pokemon')
if __name__ == '__main__':
    app.run(debug=True)
