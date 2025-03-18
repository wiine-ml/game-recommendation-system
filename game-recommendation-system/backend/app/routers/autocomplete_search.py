from flask import Blueprint, request, jsonify
from ..models import Game

autocomplete_bp = Blueprint('autocomplete_api', __name__)

@autocomplete_bp.route('/api/autocomplete/<string:query>', methods=['GET', 'POST'])
def autocomplete_search(query: str):
    print(query)
    try:
        limit = request.args.get('limit', default=5, type=int)
        result_games = Game.autocomplete_game_title(query, limit)
        print(result_games)
        return jsonify({
            'data':{
                'result_games': result_games,
            },
            'msg': 'Success',
            'code': 200,
        })
    except Exception as e:
        return jsonify({
            'data': {},
            'msg': str(e),
            'code': 500,
            })