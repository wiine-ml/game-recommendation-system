from flask import Blueprint, request, jsonify
from datetime import datetime
from database import db, SIMILARITY_METHOD

recommendation_setting_bp = Blueprint('recommendation_setting_api', __name__)

@recommendation_setting_bp.route('/api/recommendation/read', method=['POST'])
def read_recommendation_setting():
    try:
        admin_id = request.args.get('admin_id')
        new_method = request.args.get('new_method')


        if new_method == SIMILARITY_METHOD:
            return jsonify({
                'data': None,
                "msg": "推荐方法更新失败-更新前后数据一致" ,
                "success": False
                }), 500
        
        # 'cosine'或'iuf'
        if new_method == 'cosine' or new_method == 'iuf':
            SIMILARITY_METHOD == new_method
            return jsonify({
                'data': None,
                "msg": "推荐方法更新成功" ,
                "success": True
                }), 200
             
        else:
            return jsonify({
                'data': None,
                "msg": "推荐方法更新失败-未知错误" ,
                "success": False
                }), 500


        
    except BaseException as e:
            return jsonify({
                'data': None,
                "msg": f"推荐方法更新失败-错误:{str(e)}" ,
                "success": False
                }), 500