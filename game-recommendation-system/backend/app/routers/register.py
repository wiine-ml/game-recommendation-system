from flask import Blueprint, request, jsonify, current_app
from ..models import User

register_bp = Blueprint('register_api', __name__)

@register_bp.route('/api/register', methods=['POST'])
def register_user():
    try:
        # 获取请求数据
        data = request.get_json()
        email = data.get('email')
        username = data.get('username')
        password = data.get('password')
        # 基本验证
        
        if not email or not username or not password:
            return jsonify({"msg": "缺少必要字段", "success": False}), 400
        try:
            User.add(email, username, password)
            return jsonify({
                "user": {
                    "email": email,
                    "username": username
                },
                "msg": "注册成功！",
                "success": True
            }), 200
        except ValueError as e:
            return jsonify({"msg": str(e), "success": False}), 409
    except Exception as e:
        return jsonify({"msg": str(e), "success": False}), 500