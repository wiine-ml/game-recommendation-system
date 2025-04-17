from flask import Blueprint, request, jsonify, send_file
from ..models import Game, Interaction, Developer, Publisher

game_bp = Blueprint('game_api', __name__)

def construct_game_response(games, user_id=None, include_interaction=True):
    """构造游戏列表的返回数据"""
    game_list = []
    for game in games:
        # 查询用户与该游戏的交互信息（如果有用户ID参数）
        interaction = None
        if user_id and include_interaction:
            interaction = Interaction.get_by_user_and_game(user_id, game.id)

        # 统计关注者数量和评分平均分
        subscribed_count = Interaction.get_subscribed_count(game.id)
        rating_avg = Interaction.get_average_rating(game.id)

        # 构造基础游戏数据
        game_data = {
            "id": game.id,
            "gameTitle": game.gameTitle,
            "gameGenre": game.gameGenre,
            "gamePlatform": game.gamePlatform,
            "gameDeveloper": game.developers[0].DeveloperName if game.developers else None,
            "gameDeveloperID": game.developers[0].DeveloperID if game.developers else None,
            "gamePublisher": game.publishers.PublisherName if game.publishers else None,  # 获取发行商名称
            "gamePublisherID": game.publishers.PublisherID if game.publishers else None,  # 获取发行商名称
            "followers": subscribed_count if subscribed_count else 0,
            "rating": round(rating_avg, 2) if rating_avg else 0,
            "ratingPhrase": game.ratingPhrase,
            "officalRating": game.officalRating,
            "releaseYear": game.releaseYear,
            "releaseMonth": game.releaseMonth,
            "releaseDay": game.releaseDay,
            "gameImage": game.gameImage,
            "gameUrl": game.gameUrl,
            "gameDescription": game.gameDescription,  # 添加游戏描述字段
        }

        # 如果需要包含用户交互状态，添加相关字段
        if include_interaction and user_id:
            game_data.update({
                "subscribed": interaction.subscribed if interaction else False,
                "disliked": interaction.disliked if interaction else False
            })

        game_list.append(game_data)
    return game_list


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
    
    game_list = construct_game_response(items, user_id=user_id)
    
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

    include_interaction = genre != '查询游戏'
    game_list = construct_game_response(games, user_id=user_id, include_interaction=include_interaction)
    
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
    game_list = construct_game_response(items, user_id=user_id)
    
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

    # 提取游戏对象
    game_objects = [game[0] for game in games]
    game_list = construct_game_response(game_objects, user_id=user_id)

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

    # 提取游戏对象
    game_objects = [game[0] for game in games]
    game_list = construct_game_response(game_objects, user_id=user_id)

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
    game_list = construct_game_response(games, user_id=user_id)

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
        
        # 构造返回数据
        game_data = construct_game_response([target], user_id=user_id)
        return jsonify({
            "data": game_data[0] if game_data else {},
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

        # 构造返回数据
        game_list = construct_game_response([game], user_id=user_id)
        game_data = game_list[0] if game_list else {}

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

    # 提取游戏对象
    game_objects = [game[0] for game in games]
    user_id = request.args.get('user_id')
    game_list = construct_game_response(game_objects, user_id=user_id)

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
    # 提取游戏对象
    game_objects = [game[0] for game in games]
    user_id = request.args.get('user_id')
    game_list = construct_game_response(game_objects, user_id=user_id)

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
        game_list = construct_game_response([game], user_id=None, include_interaction=False)
        game_data = game_list[0] if game_list else {}

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


@game_bp.route('/api/games/read/by_publisher/page/<int:page_id>', methods=['GET'])
def read_games_by_publisher_paginated(page_id):
    """根据游戏发行商查找游戏，并支持分页"""
    publisher_id = request.args.get('publisher_id')
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10
    user_id = request.args.get('user_id')  # 可选用户ID，用于获取用户交互状态

    if not publisher_id:
        return jsonify({"error": "缺少发行商ID参数"}), 400

    # 查询指定发行商的游戏
    publisher = Publisher.query.get(publisher_id)
    if not publisher:
        return jsonify({"message": "发行商未找到"}), 404

    # 获取分页数据
    pagination = publisher.games.paginate(page=page_id, per_page=items_per_page, error_out=False)
    games = pagination.items
    total_pages = pagination.pages

    if not games:
        return jsonify({"message": "没有游戏数据"}), 200

    # 构造返回数据
    game_list = construct_game_response(games, user_id=user_id)

    return jsonify({
        'data': {
            "games": game_list,
            "totalPages": total_pages,
        },
        'msg': '查询成功',
        'success': True,
    }), 200

@game_bp.route('/api/games/read/by_developer/page/<int:page_id>', methods=['GET'])
def read_games_by_developer_paginated(page_id):
    """根据游戏开发商查找游戏，并支持分页"""
    developer_id = request.args.get('developer_id')
    print(request.args)
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认为10
    user_id = request.args.get('user_id')  # 可选用户ID，用于获取用户交互状态

    if not developer_id:
        return jsonify({"error": "缺少开发商ID参数"}), 400

    # 查询指定开发商的游戏
    developer = Developer.query.get(developer_id)
    if not developer:
        return jsonify({"message": "开发商未找到"}), 404

    # 获取分页数据
    pagination = developer.games.paginate(page=page_id, per_page=items_per_page, error_out=False)
    games = pagination.items
    total_pages = pagination.pages

    if not games:
        return jsonify({"message": "没有游戏数据"}), 200

    # 构造返回数据
    game_list = construct_game_response(games, user_id=user_id)

    return jsonify({
        'data': {
            "games": game_list,
            "totalPages": total_pages,
        },
        'msg': '查询成功',
        'success': True,
    }), 200