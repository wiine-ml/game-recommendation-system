from flask import Blueprint, request, jsonify, send_file
import os
from ..models import User, Interaction

user_bp = Blueprint('user_api', __name__)


@user_bp.route('/api/users/create', methods=['POST'])
def create_user():
    """创建用户"""
    pass


@user_bp.route('/api/users/read/page/<int:page>', methods=['GET'])
def read_page_users(page):
    """分页获取用户列表"""
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认10

    # 查询所有用户
    query = User.query
    print(type(User.query))

    # 获取总条数和总页数
    total_items = query.count()
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # 分页查询
    users = query.paginate(page=page, per_page=items_per_page, error_out=False).items

    # 构造返回数据
    user_list = []
    for user in users:
        # 获取用户所有交互记录
        interactions = Interaction.get_all_by_user(user.id)
        # 统计关注的游戏数
        subscribed_count = sum(1 for interaction in interactions if interaction.subscribed)
        # 统计评论数（评论分数不为空）
        review_count = sum(1 for interaction in interactions if interaction.review_score != 0)
        user_data = {

            "id": user.id,
            "email": user.email,
            "username": user.username,
            "avatar": user.avatar.decode('utf-8') if user.avatar else None,  # 将二进制数据转换为字符串
            "subscribed_count": subscribed_count,
            "review_count": review_count,
        }
        user_list.append(user_data)

    return jsonify({
        "data": user_list,
        "totalPages": total_pages,
        "msg": "获取分页用户列表成功",
        "success": True
    }), 200

@user_bp.route('/api/users/read/search', methods=['GET'])
def search_users():
    """根据条件搜索用户"""
    data = request.get_json()
    email = data.get('email')
    username = data.get('username')

    # 构造查询
    query = User.query
    if email:
        query = query.filter_by(email=email)
    if username:
        query = query.filter_by(username=username)

    # 获取总条数和总页数
    total_items = query.count()
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认10
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # 分页查询
    page = int(request.args.get('page', 1))  # 当前页码，默认1
    users = query.paginate(page=page, per_page=items_per_page, error_out=False).items

    # 构造返回数据
    user_list = []
    for user in users:
        interactions = Interaction.get_all_by_user(user.id)
        subscribed_count = sum(1 for interaction in interactions if interaction.subscribed)
        review_count = sum(1 for interaction in interactions if interaction.review_score != 0)
        user_data = {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "avatar": user.avatar.decode('utf-8') if user.avatar else None,  # 将二进制数据转换为字符串
            "subscribed_count": subscribed_count,
            "review_count": review_count,
        }
        user_list.append(user_data)

    return jsonify({
        "data": user_list,
        "totalPages": total_pages,
        "msg": "搜索用户成功",
        "success": True
    }), 200

@user_bp.route('/api/users/avatar/read', methods=['GET'])
def read_user_avatar():
    """获取用户头像"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "缺少用户ID参数"}), 400
    
    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    # 如果用户没有设置头像，则使用默认头像
    if not user.avatar or user.avatar == '':
        avatar_filename = "defaultUserImg.jpg"
    else:
        avatar_filename = user.avatar
    
    avatar_path = os.path.join('images', 'avatars', avatar_filename)
    print(avatar_path)
    if not os.path.exists(avatar_path):
        return jsonify({"error": "头像文件不存在"}), 404
    
    return send_file(avatar_path, mimetype='image/jpeg')

@user_bp.route('/api/users/avatar/set', methods=['POST'])
def set_user_avatar():
    """设置用户头像"""
    try:
        user_id = request.form.get('user_id')
        if not user_id:
            return jsonify({"error": "缺少用户ID参数"}), 400
        
        user = User.get_user_by_id(user_id)
        if not user:
            return jsonify({"error": "用户不存在"}), 404
        
        avatar_file = request.files.get('avatar')
        print(type(avatar_file))
        if not avatar_file:
            return jsonify({"error": "未上传头像文件"}), 400
        if avatar_file.filename == '':
            return jsonify({"error": "未选择头像文件"}), 400
        
        # 验证文件类型
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        if '.' not in avatar_file.filename or \
                avatar_file.filename.rsplit('.', 1)[1].lower() not in allowed_extensions:
            return jsonify({"error": "只允许上传图片文件（png, jpg, jpeg, gif）"}), 400
        
        # 保存头像文件
        avatar_filename = f"{user.id}_{avatar_file.filename}"
        avatar_path = os.path.join('images', 'avatars', avatar_filename)
        
        # 创建目录（如果不存在）
        os.makedirs(os.path.dirname(avatar_path), exist_ok=True)
        
        avatar_file.save(avatar_path)
        
        # 更新用户头像路径
        user.set_avatar(avatar_filename)
        
        return jsonify({"message": "头像设置成功", "avatar_path": user.avatar}), 200
    except BaseException as e:
        return jsonify({"error": str(e)}), 500

@user_bp.route('/api/users/avatar/delete', methods=['POST'])
def delete_user_avatar():
    """删除用户头像"""
    user_id = request.get_json().get('user_id')
    if not user_id:
        return jsonify({"error": "缺少用户ID参数"}), 400
    
    user = User.get_user_by_id(user_id)
    if not user:
        return jsonify({"error": "用户不存在"}), 404
    
    if not user.avatar:
        return jsonify({"error": "该用户没有设置头像"}), 404
    
    avatar_path = os.path.join('images', 'avatars', user.avatar)
    if os.path.exists(avatar_path):
        os.remove(avatar_path)
    
    # 清空用户头像路径
    user.delete_avatar()
    
    return jsonify({"message": "头像删除成功"}), 200


@user_bp.route('/api/users/update', methods=['PUT'])
def update_user():
    """更新用户信息"""
    pass


@user_bp.route('/api/users/delete', methods=['DELETE'])
def delete_user():
    """删除用户"""
    pass

