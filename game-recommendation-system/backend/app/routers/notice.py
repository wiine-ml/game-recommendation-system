from flask import Blueprint, request, jsonify
from ..models import Notice
from datetime import datetime


notice_bp = Blueprint('notice_api', __name__)


@notice_bp.route('/api/notice/create', methods=['POST'])
def create_notice():
    """创建公告"""
    data = request.get_json()
    avatar = data.get('avatar')
    username = data.get('username', '/admin.jpg')  # 默认头像
    title = data.get('title')
    content = data.get('content')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else None

    if not title or not content:
        return jsonify({"msg": "标题和内容是必填字段", "success": False}), 400

    try:
        new_notice = Notice.create_notice(avatar, username, title, content, date)
        return jsonify({
            "notice": new_notice.to_dict(),
            "msg": "公告创建成功",
            "success": True
        }), 201
    except Exception as e:
        return jsonify({"msg": str(e), "success": False}), 500
    

@notice_bp.route('/api/notice/read/<int:notice_id>', methods=['GET'])
def read_notice(notice_id):
    """根据编号获取公告"""
    notice = Notice.get_notice_by_id(notice_id)
    if not notice:
        return jsonify({"msg": "公告不存在", "success": False}), 404
    return jsonify({
        "data": notice.to_dict(),
        "msg": "获取公告成功",
        "success": True
    }), 200


@notice_bp.route('/api/notice/read/page/<int:page_id>', methods=['GET'])
def read_page_notices(page_id):
    """获取分页的公告列表"""
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认10

    # 查询所有公告
    query = Notice.query

    # 获取总条数和总页数
    total_items = query.count()
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # 分页查询
    notices = query.paginate(page=page_id, per_page=items_per_page, error_out=False).items

    # 构造返回数据
    notices_list = [notice.to_dict() for notice in notices]

    return jsonify({
        "data": {
            'notices':notices_list,
            "totalPages": total_pages,
            },
        "msg": "获取分页公告列表成功",
        "success": True
    }), 200


@notice_bp.route('/api/notice/update/<int:notice_id>', methods=['PUT'])
def update_notice(notice_id):
    """更新公告"""
    data = request.get_json()
    avatar = data.get('avatar')
    username = data.get('username')
    title = data.get('title')
    content = data.get('content')
    date = datetime.strptime(data.get('date'), '%Y-%m-%d') if data.get('date') else None
    try:
        updated_notice = Notice.update_notice(
            notice_id=notice_id,
            avatar=avatar,
            username=username,
            title=title,
            content=content,
            date=date
        )
        return jsonify({
            "notice": updated_notice.to_dict(),
            "msg": "公告更新成功",
            "success": True
        }), 200
    except ValueError as e:
        return jsonify({"msg": str(e), "success": False}), 404
    except Exception as e:
        return jsonify({"msg": str(e), "success": False}), 500


@notice_bp.route('/api/notice/delete/<int:notice_id>', methods=['DELETE'])
def delete_notice(notice_id):
    """删除公告"""
    #TODO
    pass
