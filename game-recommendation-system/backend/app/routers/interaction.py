from flask import Blueprint, request, jsonify
from ..models import Interaction

interaction_bp = Blueprint('interaction_api', __name__)


@interaction_bp.route('/api/interactions/read', methods=['GET'])
def read_user():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'error': '缺少用户ID参数'}), 400
    
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({'error': '用户ID必须是整数'}), 400
    
    # 获取用户所有交互记录
    interactions = Interaction.get_all_by_user(user_id)
    subscribed_count = sum(1 for interaction in interactions if interaction.subscribed)
    # 统计评论数（评论分数不为空）
    review_count = sum(1 for interaction in interactions if interaction.review_score != 0)
    
    return jsonify({
        'data':{
            'subscribed_count': subscribed_count,
            'review_count': review_count,
        },
        'msg': 'success',
        'success': True,
    }), 200


@interaction_bp.route('/api/interactions/update', methods=['PUT'])
def update_interaction():
    data = request.get_json()
    if not data:
        return jsonify({
            'data': None,
            'msg': 'No data provided',
            'success': False,
            }), 400
    
    user_id = data.get('user_id')
    game_id = data.get('game_id')

    if not user_id or not game_id:
        print(user_id, game_id)
        return jsonify({
            'data': None,
            'message': 'Invalid user or game id',
            'success': False,
            }), 400
    
    clicked = data.get('clicked')
    subscribed = data.get('subscribed')
    disliked = data.get('disliked')
    review_score = data.get('review_score')
    review_text = data.get('review_text')

    print(clicked, subscribed, disliked, review_score, review_text)

    interaction = Interaction.get_by_user_and_game(user_id, game_id)

    if interaction:
         # 如果存在，更新对应字段（如果字段不为空）
        update_data = {}
        if clicked is not None:
            update_data['clicked'] = clicked
        if subscribed is not None:
            update_data['subscribed'] = subscribed
        if disliked is not None:
            update_data['disliked'] = disliked
        if review_score is not None:
            update_data['review_score'] = review_score
        if review_text is not None:
            update_data['review_text'] = review_text
        
        if update_data:
            Interaction.update(interaction.id, **update_data)
            return jsonify({
                "message": "交互记录更新成功",
                "interaction_id": interaction.id,
                "data":{
                    "clicked": interaction.clicked,
                    "subscribed": interaction.subscribed,
                    "disliked": interaction.disliked,
                    "review_score": interaction.review_score,
                    "review_text": interaction.review_text
                },
                'success': True,
                }), 200
        else:
            return jsonify({
                'data': None,
                "message": "没有需要更新的字段",
                'success': True,
                }), 200
    else:
        # 如果不存在，创建新的 interaction 记录
        new_interaction_id = Interaction.create(
            user_id=user_id,
            game_id=game_id,
            clicked=clicked if clicked is not None else False,
            subscribed=subscribed if subscribed is not None else False,
            disliked=disliked if disliked is not None else False,
            review_score=review_score if review_score is not None else 0,
            review_text=review_text if review_text is not None else ""
        )
        return jsonify({
            "data": new_interaction_id,
            "message": "交互记录创建成功",
            'success': True,
            }), 201


@interaction_bp.route('/api/interactions/delete', methods=['DELETE'])
def delete_interaction():
    #TODO
    pass