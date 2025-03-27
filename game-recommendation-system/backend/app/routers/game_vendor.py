from flask import Blueprint, request, jsonify, send_file
from ..models import Game, Interaction, Developer, Publisher, game_developers, game_publishers
from database import db

game_vendor_bp = Blueprint('game_vendor_api', __name__)

def get_vendor_model(vendor_type, vendor_id):
    if vendor_type == 'developer':
        return Developer.get_developer_by_id(vendor_id)
    elif vendor_type == 'publisher':
        return Publisher.get_publisher_by_id(vendor_id)
    return None

@game_vendor_bp.route('/api/game_vendor/promoted_game/add', methods=['POST'])
def add_vendor_promoted_image():
    """添加厂商推广图片"""
    try:
        game_id = request.json.get('game_id')
        vendor_id = request.json.get('vendor_id')
        vendor_type = request.json.get('vendor_type')

        # 检查参数是否完整
        if not all([game_id, vendor_id, vendor_type]):
            return jsonify({"error": "缺少必要参数"}), 400

        # 检查 vendor_type 是否有效
        if vendor_type not in ['developer', 'publisher']:
            return jsonify({"error": "无效的厂商类型"}), 400

        # 检查 game_id 是否属于该厂商
        if vendor_type == 'developer':
            # 查询 game_developers 表，检查是否存在对应的记录
            record = db.session.query(game_developers).filter_by(GameID=game_id, DeveloperID=vendor_id).first()
        else:
            # 查询 game_publishers 表，检查是否存在对应的记录
            record = db.session.query(game_publishers).filter_by(GameID=game_id, PublisherID=vendor_id).first()

        if not record:
            return jsonify({"error": "游戏不属于该厂商，无法添加推广"}), 403

        # 检查是否已有超过五个推广游戏
        if vendor_type == 'developer':
            promoted_count = db.session.query(game_developers).filter_by(DeveloperID=vendor_id, is_promoted=True).count()
        else:
            promoted_count = db.session.query(game_publishers).filter_by(PublisherID=vendor_id, is_promoted=True).count()

        if promoted_count >= 5:
            return jsonify({"error": "推广游戏数量已达到上限（5个），无法添加更多推广"}), 400

        # 更新 is_promoted 字段为 True
        if vendor_type == 'developer':
            db.session.query(game_developers).filter_by(GameID=game_id, DeveloperID=vendor_id).update({'is_promoted': True})
        else:
            db.session.query(game_publishers).filter_by(GameID=game_id, PublisherID=vendor_id).update({'is_promoted': True})

        db.session.commit()

        return jsonify({"message": "添加推广成功"}), 200

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500
    
@game_vendor_bp.route('/api/vendor/promoted_game/delete', methods=['DELETE'])
def delete_vendor_promoted_image():
    """删除厂商推广图片"""
    try:
        game_id = request.json.get('game_id')
        vendor_id = request.json.get('vendor_id')
        vendor_type = request.json.get('vendor_type')

        # 检查参数是否完整
        if not all([game_id, vendor_id, vendor_type]):
            return jsonify({"error": "缺少必要参数"}), 400

        # 检查 vendor_type 是否有效
        if vendor_type not in ['developer', 'publisher']:
            return jsonify({"error": "无效的厂商类型"}), 400

        # 检查 game_id 是否属于该厂商
        if vendor_type == 'developer':
            # 查询 game_developers 表，检查是否存在对应的记录
            record = db.session.query(game_developers).filter_by(GameID=game_id, DeveloperID=vendor_id).first()
        else:
            # 查询 game_publishers 表，检查是否存在对应的记录
            record = db.session.query(game_publishers).filter_by(GameID=game_id, PublisherID=vendor_id).first()

        if not record:
            return jsonify({"error": "游戏不属于该厂商，无法删除推广"}), 403

        # 更新 is_promoted 字段为 False
        if vendor_type == 'developer':
            db.session.query(game_developers).filter_by(GameID=game_id, DeveloperID=vendor_id).update({'is_promoted': False})
        else:
            db.session.query(game_publishers).filter_by(GameID=game_id, PublisherID=vendor_id).update({'is_promoted': False})

        db.session.commit()

        return jsonify({"message": "删除推广成功"}), 200

    except Exception as e:
        db.session.rollback()
        print(str(e))
        return jsonify({"error": str(e)}), 500