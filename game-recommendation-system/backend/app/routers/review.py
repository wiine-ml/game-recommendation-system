from flask import Blueprint, request, jsonify, current_app
from ..models import Interaction, Game

review_bp = Blueprint('review_api', __name__)

@review_bp.route('/api/reviews/create', methods=['POST'])
def create_review():
    """创建评论"""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    review_score = data.get('review_score')
    review_text = data.get('review_text')

    print(user_id, game_id, review_score, review_text)

    if not user_id or not game_id:
        return jsonify({'message': 'Invalid user or game id'}), 400
    
    # 检查用户是否已经对游戏进行过评论
    existing_interaction = Interaction.get_by_user_and_game(user_id, game_id)
    if existing_interaction:
        if existing_interaction.review_score == 0 and existing_interaction.review_text is '':
            # 如果没有评论，更新交互记录
            update_data = {}
            if review_score is not None:
                update_data['review_score'] = review_score
            if review_text is not None:
                update_data['review_text'] = review_text
            
            if update_data:
                Interaction.update(existing_interaction.id, **update_data)
                return jsonify({
                    "message": "评论更新成功",
                    "interaction_id": existing_interaction.id,
                    "data": {
                        "review_score": review_score,
                        "review_text": review_text
                    }
                }), 200
            else:
                return jsonify({"message": "没有需要更新的字段"}), 200
        else:
            return jsonify({'message': '用户已经对该游戏进行过评论'}), 400
    else:
        # 创建新的交互记录
        new_interaction_id = Interaction.create(
            user_id=user_id,
            game_id=game_id,
            clicked=False,
            subscribed=False,
            disliked=False,
            review_score=review_score,
            review_text=review_text
        )
        return jsonify({"message": "评论创建成功", "interaction_id": new_interaction_id}), 201
    

@review_bp.route('/api/reviews/read', methods=['GET'])
def read_reviews():
    """获取指定用户的全部评论"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'message': 'Missing user_id parameter'}), 400
    
    try:
        user_id = int(user_id)
    except ValueError as e:
        return jsonify({'message': 'Invalid user_id format'+str(e)}), 400
    
    # 获取用户的所有交互记录
    interactions = Interaction.get_all_by_user(user_id)
    
    # 提取评论信息
    reviews = []
    for interaction in interactions:
        if interaction.review_score != 0 or interaction.review_text is not '':
            # 查询游戏名称
            game = Game.get_game_by_id(interaction.game_id)
            game_title = game.gameTitle if game else '游戏不存在'

            reviews.append({
                'game_id': interaction.game_id,
                'game_title': game_title,
                'review_score': interaction.review_score,
                'review_text': interaction.review_text,
                'created_at': interaction.created_at.isoformat() if interaction.created_at else None,
            })
    
    return jsonify({
        'message': 'Reviews retrieved successfully',
        'reviews': reviews
    }), 200


@review_bp.route('/api/reviews/read/page/<int:page_id>', methods=['GET'])
def read_page_reviews(page_id):
    """获取指定页的评论"""
    #TODO: 实现分页功能
    pass



@review_bp.route('/api/reviews/read/search', methods=['GET'])
def search_review():
    """获取用户某条评论"""
    user_id = request.args.get('user_id')
    game_id = request.args.get('game_id')

    if not user_id or not game_id:
        return jsonify({'message': 'Invalid user or game id'}), 400
    
    # 获取交互记录
    interaction = Interaction.get_by_user_and_game(user_id, game_id)
    if not interaction:
        return jsonify({'message': '交互记录不存在'}), 404
    
    # 返回评论信息
    return jsonify({
        "message": "评论获取成功",
        "data": {
            "review_score": interaction.review_score,
            "review_text": interaction.review_text
        }
    }), 200


@review_bp.route('/api/reviews/update', methods=['PUT'])
def update_review():
    """更新评论"""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    user_id = data.get('user_id')
    game_id = data.get('game_id')
    review_score = data.get('review_score')
    review_text = data.get('review_text')

    if not user_id or not game_id:
        return jsonify({'message': 'Invalid user or game id'}), 400
    
    # 获取交互记录
    interaction = Interaction.get_by_user_and_game(user_id, game_id)
    if not interaction:
        return jsonify({'message': '交互记录不存在'}), 404
    
    # 更新评论
    update_data = {}
    if review_score is not None:
        update_data['review_score'] = review_score
    if review_text is not None:
        update_data['review_text'] = review_text
    
    if update_data:
        Interaction.update(interaction.id, **update_data)
        return jsonify({
            "message": "评论更新成功",
            "interaction_id": interaction.id,
            "data": {
                "review_score": interaction.review_score,
                "review_text": interaction.review_text
            }
        }), 200
    else:
        return jsonify({"message": "没有需要更新的字段"}), 200


@review_bp.route('/api/reviews/delete/<int:game_id>', methods=['DELETE'])
def delete_review(game_id):
    """删除评论"""
    data = request.get_json()
    if not data:
        return jsonify({'message': 'No data provided'}), 400
    
    user_id = data.get('user_id')
    if not user_id:
        return jsonify({'message': 'Invalid user id'}), 400
    
    # 获取交互记录
    result = Interaction.delete_reviews(Interaction.get_by_user_and_game(user_id, game_id).id)
    if result < 0:
        return jsonify({'message': '评论删除失败'}), 500

    return jsonify({"message": "评论删除成功"}), 200