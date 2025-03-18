from flask import Blueprint, jsonify


test_bp = Blueprint('test_api', __name__)

# Test API
# 请求所有资源时无需路由参数
# 请求单个资源时需传入资源ID作为路由参数
@test_bp.route('/api/test', methods=['GET', 'POST', 'PUT', 'DELETE'])
def connectivity_testing():
    try:
        response = {
        "data": {},
        "msg": 'Connection successful',
        "success": True,
        }
        return jsonify(response), 200
    except Exception as e:
        response = {
        "data": {},
        "msg": 'Connection failed',
        "success": False,
        }
        return jsonify(response), 500
    
