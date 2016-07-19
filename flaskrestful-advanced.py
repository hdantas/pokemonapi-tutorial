from flask import Flask
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

pokedex = [{
    'number': 14,
    'name': 'Kakuna',
    'type': ['bug', 'poison'],
    'weaknesses': ['fire', 'flying', 'psychic', 'rock'],
    'evolutions': [{'number': 15, 'name': 'beedrill'}]
}, {
    'number': 16,
    'name': 'Pidgey',
    'type': ['normal', 'flying'],
    'weaknesses': ['electric', 'ice', 'rock'],
    'evolutions': [{'number': 17, 'name': 'Pidgeotto'},
                   {'number': 18, 'name': 'Pidgeot'}]
}, {
    'number': 51,
    'name': 'Dugtrio',
    'type': ['ground'],
    'weaknesses': ['grass', 'ice', 'water'],
    'evolutions': []
}]


def list_of_strings(value):
    all_str = isinstance(value, list) and all([isinstance(v, basestring) for v in value])
    if not all_str:
        raise ValueError("Not all items are strings")
    return value


def get_pokemon_args():
    root_parser = reqparse.RequestParser()
    root_parser.add_argument('name', required=True, type=str, location='json')
    root_parser.add_argument('number', required=True, type=int, location='json')

    root_parser.add_argument('type', required=True, type=list_of_strings, location='json')
    root_parser.add_argument('weaknesses', required=True, type=list_of_strings, location='json')
    root_parser.add_argument('evolutions', required=True, type=list, location='json')

    root_args = root_parser.parse_args(strict=True)

    for evolution in root_args.get('evolutions'):
        evolutions_parser = reqparse.RequestParser()
        evolutions_parser.add_argument('name', required=True, type=str, location='evolution')
        evolutions_parser.add_argument('number', required=True, type=int, location='evolution')

        evolution_arg = reqparse.Namespace()
        evolution_arg.evolution = evolution
        evolutions_parser.parse_args(req=evolution_arg, strict=True)

    return root_args


class Pokemon(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('number', required=False, type=int, location='args')

        args = parser.parse_args(strict=True)
        number = args.get('number')
        if number is not None:
            if number in [pokemon['number'] for pokemon in pokedex]:
                return [pokemon for pokemon in pokedex if pokemon['number'] == number][0]
            else:
                return {}

        return pokedex

    def post(self):
        args = get_pokemon_args()

        new_pokemon = {
            'name': args['name'],
            'number': args['number'],
            'type': args['type'],
            'weaknesses': args['weaknesses'],
            'evolutions': args['evolutions']
        }

        number = new_pokemon['number']
        all_numbers = [pokemon['number'] for pokemon in pokedex]
        if number in all_numbers or new_pokemon in pokedex:
            return {}

        pokedex.append(new_pokemon)
        return pokedex[-1]

    def put(self):
        root_args = get_pokemon_args()

        new_pokemon = {
            'name': root_args['name'],
            'number': root_args['number'],
            'type': root_args['type'],
            'weaknesses': root_args['weaknesses'],
            'evolutions': root_args['evolutions']
        }

        number = new_pokemon['number']
        all_numbers = [pokemon['number'] for pokemon in pokedex]
        if number not in all_numbers or new_pokemon in pokedex:
            return {}

        pokedex_index = all_numbers.index(number)
        pokedex[pokedex_index] = new_pokemon

        return pokedex[pokedex_index]

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('number', type=int, required=True, location='args')
        args = parser.parse_args(strict=True)
        success = False

        number = args['number']

        all_numbers = [pokemon['number'] for pokemon in pokedex]
        if number in all_numbers:
            pokedex[:] = [pokemon for pokemon in pokedex if pokemon.get('number') != number]
            success = True

        return {'success': success}


api.add_resource(Pokemon, '/api/v2/pokemon')

if __name__ == '__main__':
    app.run(debug=True)
