from flask import Blueprint, request, jsonify
from ..models import Interaction, Game

from ..utils.user_based_CF import get_user_interaction_matrix, improved_cosine_similarity, generate_game_recommendations
from ..utils.item_based_CF import get_item_interaction_matrix, calculate_item_similarity, generate_item_recommendations


import time  # 用于记录时间


recommendation_bp = Blueprint('recommendation_api', __name__)


@recommendation_bp.route('/api/recommendations/read', methods=['GET'])
def read_recommendations():
    """获取游戏推荐"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "缺少用户ID参数"}), 400
    
    try:
        user_id = int(user_id)
    except ValueError:
        return jsonify({"error": "用户ID必须是整数"}), 400
    
    # 检查用户交互数据数量
    interaction_count = Interaction.query.filter_by(user_id=user_id).count()
    if interaction_count < 5:
        return jsonify({
            "recommendations": [],
            "msg": "你的交互记录太少了，先去浏览一下游戏吧",
            'success': True,
            }), 200

    selected_method = 'item_based_CF'


    # 开始计算推荐时间
    start_time = time.time()
    print(f"开始计算推荐时间: {start_time}")

    if selected_method == 'user_based_CF':
        #生成推荐
        user_interaction_matrix = get_user_interaction_matrix()
        similar_users = improved_cosine_similarity(user_interaction_matrix, user_id, n=5)
        recommendations = generate_game_recommendations(user_interaction_matrix, user_id, similar_users, top_n=10)
        recommended_game_ids = [game_id for game_id, _ in recommendations]
        #通过id获取推荐游戏信息
        recommended_games = Game.query.filter(Game.id.in_(recommended_game_ids)).all()
    elif selected_method == 'item_based_CF':
        # item-based CF 推荐算法
        # 获取物品交互矩阵
        item_interaction_matrix = get_item_interaction_matrix()

        # 计算物品相似度矩阵
        item_similarity_matrix = calculate_item_similarity(item_interaction_matrix)

        # 为用户生成推荐
        recommendations = generate_item_recommendations(user_id, item_interaction_matrix, item_similarity_matrix, top_n=20, top_k=20)

        # 提取推荐的物品ID
        recommended_item_ids = [item_id for item_id, _ in recommendations]

        # 通过ID获取推荐游戏信息
        recommended_games = Game.query.filter(Game.id.in_(recommended_item_ids)).all()


    print(type(recommended_games))
    print(type(recommended_games[0]))
    print(recommended_games)
    print('---'*5)



    # 结束计算推荐时间
    end_time = time.time()
    print(f"结束计算推荐时间: {end_time}")
    # 计算推荐算法计算时长
    duration = end_time - start_time
    print(f"推荐算法计算时长: {duration}秒")

    # 构造返回数据
    game_list = []
    for game in recommended_games:
        interaction = Interaction.get_by_user_and_game(user_id, game.id)
        subscribed_count = Interaction.get_subscribed_count(game.id)
        rating_avg = Interaction.get_average_rating(game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.developers.DeveloperName if game.developers else None,
            "gamePublisher": game.publishers.PublisherName if game.publishers else None,  # 获取发行商名称
            "followers": subscribed_count,
            "rating": rating_avg,
            "ratingPhrase": game.ratingPhrase,
            "officalRating": game.officalRating,
            "releaseYear": game.releaseYear,
            "releaseMonth": game.releaseMonth,
            "releaseDay": game.releaseDay,
            "gameImage": game.gameImage,
            "gameUrl": game.gameUrl,

            "subscribed": interaction.subscribed if interaction else False, 
            "disliked": interaction.disliked if interaction else False
        }
        game_list.append(game_data)

    # 如果推荐的游戏列表为空
    if not game_list:
        return jsonify({
            "recommendations": [], 
            "msg": "暂未找到适合你的数据，先看看热门游戏吧"
            }), 200
    
    return jsonify({
        "recommendations": game_list,
        "msg": "为你推荐以下游戏",
    }), 200