from flask import Blueprint, request, jsonify, send_file
from ..models import Game, Interaction
import os
from PIL import Image

game_bp = Blueprint('game_api', __name__)


@game_bp.route('/api/games/create', methods=['POST'])
def create_game():
    """创建游戏"""
    pass


@game_bp.route('/api/games/read/subscribed', methods=['GET'])
def read_subscribed_game():
    """获取用户关注的所有游戏，并支持分页"""
    user_id = request.args.get('user_id')
    page_id = int(request.args.get('page_id', 1))  # 当前页码，默认为1
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10

    if not user_id:
        return jsonify({"error": "缺少用户ID参数"}), 400
    
    # 查询用户所有交互记录中 subscribed 为 True 的记录
    interactions = Interaction.query.filter_by(user_id=user_id, subscribed=True).all()
    
    if not interactions:
        return jsonify({"message": "用户没有关注任何游戏"}), 200
    
    # 获取所有关注的游戏的 ID
    game_ids = [interaction.game_id for interaction in interactions]
    
    # 查询这些游戏的详细信息，并支持分页
    games = Game.query.filter(Game.id.in_(game_ids)).paginate(
        page=page_id, 
        per_page=items_per_page, 
        error_out=False
    )

    # 获取总页数
    total_pages = games.pages
    current_page = games.page
    items = games.items
    
    if not items:
        return jsonify({"message": "用户没有关注任何游戏"}), 200
    
    # 构造返回数据
    game_list = []
    for game in games:
        # 查询用户与该游戏的交互信息
        interaction = Interaction.get_by_user_and_game(user_id, game.id)

        # 统计关注者数量和评分平均分
        subscribed_count = Interaction.get_subscribed_count(game.id)
        rating_avg = Interaction.get_average_rating(game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count,
            "rating": rating_avg,
            "ratingPhrase": game.ratingPhrase,
            "officalRating": game.officalRating,
            "releaseYear": game.releaseYear,
            "releaseMonth": game.releaseMonth,
            "releaseDay": game.releaseDay,
            "gameImage": game.gameImage,
            "gameUrl": game.gameUrl,

            "subscribed": interaction.subscribed if interaction else False,  # 用户订阅状态
            "disliked": interaction.disliked if interaction else False# 用户不喜欢状态
        }
        game_list.append(game_data)
    
    return jsonify({
        "games": game_list,
        "totalPages": total_pages
    }), 200


@game_bp.route('/api/games/read/page/<int:page_id>', methods=['GET'])
def read_page_game(page_id):
    """根据游戏类型查找游戏，并支持分页"""
    genre = request.args.get('type')
    items_per_page = int(request.args.get('itemPerpage', 10))
    user_id = request.args.get('user_id')

    if not genre:
        return jsonify({"error": "缺少游戏类型参数"}), 400
    
    print(genre)
    
    # 查询所有游戏或按类型查询游戏
    if genre == '全部' or genre == '查询游戏':
        query = Game.query
        
    else:
        query = Game.query.filter_by(gameGenre=genre)

    
    # 获取总页数
    total_items = query.count()
    total_pages = (total_items + items_per_page - 1) // items_per_page
    games = query.paginate(page=page_id, per_page=items_per_page, error_out=False).items

    # 构造返回数据
    game_list = []
    for game in games:
        # 查询用户与该游戏的交互信息
        interaction = Interaction.get_by_user_and_game(user_id, game.id)

        # 统计关注者数量和评分平均分
        subscribed_count = Interaction.get_subscribed_count(game.id)
        rating_avg = Interaction.get_average_rating(game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count,
            "rating": rating_avg,
            "ratingPhrase": game.ratingPhrase,
            "officalRating": game.officalRating,
            "releaseYear": game.releaseYear,
            "releaseMonth": game.releaseMonth,
            "releaseDay": game.releaseDay,
            "gameImage": game.gameImage,
            "gameUrl": game.gameUrl,
        }

        # 如果 genre 不是 '查询游戏'，则添加 subscribed 和 disliked 字段
        if genre != '查询游戏':
            
            game_data.update({
                "subscribed": interaction.subscribed if interaction else False,
                "disliked": interaction.disliked if interaction else False
            })
        game_list.append(game_data)
    
    return jsonify({
        "data": {
            "games": game_list,
            "totalPages": total_pages,
        },
        "msg": "获取分页游戏列表成功",
        "success": True
    }), 200


@game_bp.route('/api/games/read/subscribed/page/<int:page_id>', methods=['GET'])
def read_subscribed_game_paginated(page_id):
    """获取用户关注的游戏分页列表"""
    user_id = request.args.get('user_id')
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10

    if not user_id:
        return jsonify({"error": "缺少用户ID参数"}), 400
    
    # 查询用户所有交互记录中 subscribed 为 True 的记录
    interactions = Interaction.query.filter_by(user_id=user_id, subscribed=True).all()
    
    if not interactions:
        return jsonify({"message": "用户没有关注任何游戏"}), 200
    
    # 获取所有关注的游戏的 ID
    game_ids = [interaction.game_id for interaction in interactions]
    
    # 查询这些游戏的详细信息，并支持分页
    games_pagination = Game.query.filter(Game.id.in_(game_ids)).paginate(
        page=page_id, 
        per_page=items_per_page, 
        error_out=False
    )

    # 获取总页数和当前页数据
    total_pages = games_pagination.pages
    current_page = games_pagination.page
    items = games_pagination.items
    
    if not items:
        return jsonify({"message": "用户没有关注任何游戏"}), 200
    
    # 构造返回数据
    game_list = []
    for game in items:
        # 查询用户与该游戏的交互信息
        interaction = Interaction.get_by_user_and_game(user_id, game.id)

        # 统计关注者数量和评分平均分
        subscribed_count = Interaction.get_subscribed_count(game.id)
        rating_avg = Interaction.get_average_rating(game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count,
            "rating": rating_avg,
            "ratingPhrase": game.ratingPhrase,
            "officalRating": game.officalRating,
            "releaseYear": game.releaseYear,
            "releaseMonth": game.releaseMonth,
            "releaseDay": game.releaseDay,
            "gameImage": game.gameImage,
            "gameUrl": game.gameUrl,

            "subscribed": interaction.subscribed if interaction else False,  # 用户订阅状态
            "disliked": interaction.disliked if interaction else False  # 用户不喜欢状态
        }
        game_list.append(game_data)
    
    return jsonify({
        'data':{
            "games": game_list,
            "totalPages": total_pages,
            "currentPage": current_page
        },
        "msg": "获取分页游戏列表成功",
        "success": True,
    }), 200


@game_bp.route('/api/games/read/top_rated/page/<int:page_id>', methods=['GET'])
def read_top_rated_games_paginated(page_id):
    """获取根据评分平均分排序的游戏分页列表"""
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10
    user_id = request.args.get('user_id')  # 可选用户ID，用于获取用户交互状态

    # 调用 Game 类中的方法获取分页数据
    pagination = Game.get_top_rated_games(page=page_id, per_page=items_per_page)
    games = pagination.items
    total_pages = pagination.pages

    if not games:
        return jsonify({"message": "没有游戏数据"}), 200

    # 构造返回数据
    game_list = []
    for game, subscribed_count, rating_avg in games:
        # 查询用户与该游戏的交互信息（如果有用户ID参数）
        interaction = None
        if user_id:
            interaction = Interaction.get_by_user_and_game(user_id, game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count if subscribed_count else 0,
            "rating": round(rating_avg, 2) if rating_avg else 0,
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

    return jsonify({
        'data': {
            "games": game_list,
            "totalPages": total_pages,
        },
        'msg': '查询成功',
        'success': True,
    }), 200


@game_bp.route('/api/games/read/top_subscribed/page/<int:page_id>', methods=['GET'])
def read_top_subscribed_games_paginated(page_id):
    """获取根据关注者数量排序的游戏分页列表"""
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10
    user_id = request.args.get('user_id')  # 可选用户ID，用于获取用户交互状态

    # 调用 Game 类中的方法获取分页数据
    pagination = Game.get_top_subscribed_games(page=page_id, per_page=items_per_page)
    games = pagination.items
    total_pages = pagination.pages

    if not games:
        return jsonify({"message": "没有游戏数据"}), 200

    # 构造返回数据
    game_list = []
    for game, subscribed_count, rating_avg in games:
        # 查询用户与该游戏的交互信息（如果有用户ID参数）
        interaction = None
        if user_id:
            interaction = Interaction.get_by_user_and_game(user_id, game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count if subscribed_count else 0,
            "rating": round(rating_avg, 2) if rating_avg else 0,
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

    return jsonify({
        'data': {
            "games": game_list,
            "totalPages": total_pages,
        },
        'msg': '查询成功',
        'success': True,
    }), 200


@game_bp.route('/api/games/read/recently/page/<int:page_id>', methods=['GET'])
def read_recently_games_paginated(page_id):
    """获取最近更新的游戏分页列表"""
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10
    user_id = request.args.get('user_id')  # 可选用户ID，用于获取用户交互状态

    # 调用 Game 类中的方法获取分页数据
    pagination = Game.get_recently_updated_games(page=page_id, per_page=items_per_page)
    games = pagination.items
    total_pages = pagination.pages

    if not games:
        return jsonify({"message": "没有游戏数据"}), 200

    # 构造返回数据
    game_list = []
    for game in games:
        # 查询用户与该游戏的交互信息（如果有用户ID参数）
        interaction = None
        if user_id:
            interaction = Interaction.get_by_user_and_game(user_id, game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": game.followers,
            "rating": round(game.rating, 2) if game.rating else 0,
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

    return jsonify({
        'data': {
            "games": game_list,
            "totalPages": total_pages,
        },
        'msg': '查询成功',
        'success': True,
    }), 200
    

@game_bp.route('/api/games/read/search/<string:game_title>', methods=['GET'])
def search_game_by_title(game_title):
    """根据游戏标题搜索游戏"""
    try:
        user_id = request.args.get('user_id')
        target = Game.get_game_by_title(game_title)
        if not target:
            return jsonify({"error": "游戏未找到"}), 404
        return jsonify({
            "data": {
                "id": target.id,
                "gameTitle": target.gameTitle,
                "gameGenre": target.gameGenre,
                "gamePlatform": target.gamePlatform,
                "gameDeveloper": target.gameDeveloper,
                "gamePublisher": target.gamePublisher,
                "ratingPhrase": target.ratingPhrase,
                "officalRating": target.officalRating,
                "releaseYear": target.releaseYear,
                "releaseMonth": target.releaseMonth,
                "releaseDay": target.releaseDay,
                "gameImage": target.gameImage,
                "gameUrl": target.gameUrl,
            },
            "msg": '查询成功',
            'success': True
        }), 200
    except Exception as e:
        return jsonify({
            "data": [],
            "msg": str(e),
        }), 500


@game_bp.route('/api/games/read/search', methods=['GET'])
def search_game():
    """根据游戏ID获取游戏详情"""
    try:
        user_id = request.args.get('user_id')
        game_id = request.args.get('game_id')

        # 查询游戏基本信息
        game = Game.query.get(game_id)
        if not game:
            return jsonify({"error": "游戏未找到"}), 404

        # 查询用户与该游戏的交互信息
        interaction = Interaction.get_by_user_and_game(user_id, game.id) if user_id else None

        # 统计关注者数量和评分平均分
        subscribed_count = Interaction.get_subscribed_count(game.id)
        rating_avg = Interaction.get_average_rating(game.id)

        # 构造返回数据
        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count,
            "rating": rating_avg,
            "ratingPhrase": game.ratingPhrase,
            "officalRating": game.officalRating,
            "releaseYear": game.releaseYear,
            "releaseMonth": game.releaseMonth,
            "releaseDay": game.releaseDay,
            "gameImage": game.gameImage,
            "gameUrl": game.gameUrl,
            "subscribed": interaction.subscribed if interaction else False,  # 用户订阅状态
            "disliked": interaction.disliked if interaction else False  # 用户不喜欢状态
        }

        return jsonify({
            "data": game_data,
            "msg": '查询成功',
        }), 200
    except Exception as e:
        return jsonify({
            "data": [],
            "msg": str(e),
        }), 500


@game_bp.route('/api/games/read/top_subscribed', methods=['GET'])
def read_top_subscribed_games():
    """获取根据关注者数量排序的所有游戏，并支持分页"""
    page_id = int(request.args.get('page_id', 1))  # 当前页码，默认为1
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10

    # 调用 Game 类中的方法获取分页数据
    pagination = Game.get_top_subscribed_games(page=page_id, per_page=items_per_page)
    games = pagination.items
    total_pages = pagination.pages

    if not games:
        return jsonify({"message": "没有游戏数据"}), 200

    # 构造返回数据
    game_list = []
    for game, subscribed_count, rating_avg in games:
        # 查询用户与该游戏的交互信息（如果有用户ID参数）
        user_id = request.args.get('user_id')
        interaction = None
        if user_id:
            interaction = Interaction.get_by_user_and_game(user_id, game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count if subscribed_count else 0,
            "rating": round(rating_avg, 2) if rating_avg else 0,
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

    return jsonify({
        "games": game_list,
        "totalPages": total_pages
    }), 200


@game_bp.route('/api/games/read/top_rated', methods=['GET'])
def read_top_rated_games():
    """获取根据评分平均分排序的所有游戏，并支持分页"""
    page_id = int(request.args.get('page_id', 1))  # 当前页码，默认为1
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10

    # 调用 Game 类中的方法获取分页数据
    pagination = Game.get_top_rated_games(page=page_id, per_page=items_per_page)
    games = pagination.items
    total_pages = pagination.pages

    if not games:
        return jsonify({"message": "没有游戏数据"}), 200

    # 构造返回数据
    game_list = []
    for game, subscribed_count, rating_avg in games:
        # 查询用户与该游戏的交互信息（如果有用户ID参数）
        user_id = request.args.get('user_id')
        interaction = None
        if user_id:
            interaction = Interaction.get_by_user_and_game(user_id, game.id)

        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "followers": subscribed_count if subscribed_count else 0,
            "rating": round(rating_avg, 2) if rating_avg else 0,
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

    return jsonify({
        "games": game_list,
        "totalPages": total_pages
    }), 200


@game_bp.route('/api/games/read/<int:game_id>', methods=['GET'])
def read_game_details(game_id):
    """根据游戏ID获取游戏所有信息"""
    try:
        # 查询游戏基本信息
        game = Game.query.get(game_id)
        if not game:
            return jsonify({"error": "游戏未找到"}), 404

        # 构造返回数据
        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.gameDeveloper,
            "gamePublisher": game.gamePublisher,
            "ratingPhrase": game.ratingPhrase,
            "officalRating": game.officalRating,
            "releaseYear": game.releaseYear,
            "releaseMonth": game.releaseMonth,
            "releaseDay": game.releaseDay,
            "gameImage": game.gameImage,
            "gameUrl": game.gameUrl,
        }

        return jsonify({
            "data": game_data,
            "msg": '查询成功',
            'success': True
        }), 200
    except Exception as e:
        return jsonify({
            "data": [],
            "msg": str(e),
        }), 500
    

@game_bp.route('/api/games/update/<int:game_id>', methods=['PUT'])
def update_game(game_id):
    """更新游戏信息"""
    pass


@game_bp.route('/api/games/delete/<int:game_id>', methods=['DELETE'])
def delete_game(game_id):
    """删除游戏"""
    pass



@game_bp.route('/api/games/rating_distribution/<int:game_id>', methods=['GET'])
def get_rating_distribution(game_id):
    """统计游戏的评分分布"""
    try:
        # 查询指定游戏的所有评分记录
        ratings = Interaction.query.filter_by(game_id=game_id).all()
        
        # 初始化五个评分区间的计数器
        rating_distribution = {
            '0-1': 0,
            '1-2': 0,
            '2-3': 0,
            '3-4': 0,
            '4-5': 0
        }
        
        # 遍历评分记录，统计每个区间的数量
        for rating in ratings:
            if rating.review_score is not None:
                score = float(rating.review_score)
                if 0 < score < 1:
                    rating_distribution['0-1'] += 1
                elif 1 <= score < 2:
                    rating_distribution['1-2'] += 1
                elif 2 <= score < 3:
                    rating_distribution['2-3'] += 1
                elif 3 <= score < 4:
                    rating_distribution['3-4'] += 1
                elif 4 <= score <= 5:
                    rating_distribution['4-5'] += 1
        
        return jsonify({
            'data': rating_distribution,
            'msg': '查询成功',
            'success': True
        }), 200
    
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500
