from flask import Blueprint, request, jsonify
from ..models import Administrator

administrator_bp = Blueprint('administrator_api', __name__)


@administrator_bp.route('/api/admin/create', methods=['POST'])
def create_admin():
    """创建新管理员"""
    data = request.get_json()
    admin_type = data.get('admin_type')
    admin_name = data.get('admin_name')
    password = data.get('password')

    # 验证请求数据
    if not admin_type or not admin_name or not password:
        return jsonify({"msg": "缺少必填参数", "success": False}), 400

    try:
        # 创建新管理员
        new_admin = Administrator.add(admin_type, admin_name, password)
        return jsonify({
            "data": {
                "id": new_admin.id,
                "admin_type": new_admin.admin_type,
                "admin_name": new_admin.admin_name
            },
            "msg": "管理员创建成功",
            "success": True
        }), 201
    except ValueError as e:
        return jsonify({"msg": str(e), "success": False}), 400
    except Exception as e:
        return jsonify({"msg": str(e), "success": False}), 500


@administrator_bp.route('/api/admin/read/page/<int:page>', methods=['GET'])
def read_page_admin(page):
    """分页获取管理员列表"""
    items_per_page = int(request.args.get('itemPerpage', 10))  # 每页显示的条数，默认10

    # 查询所有管理员
    query = Administrator.query

    # 获取总条数和总页数
    total_items = query.count()
    total_pages = (total_items + items_per_page - 1) // items_per_page

    # 分页查询
    admins = query.paginate(page=page, per_page=items_per_page, error_out=False).items

    # 构造返回数据
    admin_list = []
    for admin in admins:
        admin_data = {
            "id": admin.id,
            "admin_type": admin.admin_type,
            "admin_name": admin.admin_name
        }
        admin_list.append(admin_data)

    return jsonify({
        "data": admin_list,
        "totalPages": total_pages,
        "msg": "获取分页管理员列表成功",
        "success": True
    }), 200


@administrator_bp.route('/api/admin/read/<int:admin_id>', methods=['GET'])
def read_admin(admin_id):
    """获取管理员信息"""
    # 查询管理员
    pass

@administrator_bp.route('/api/admin/update/<int:admin_id>', methods=['PUT'])
def update_admin(admin_id):
    """更新管理员信息"""
    pass

@administrator_bp.route('/api/admin/delete/<int:admin_id>', methods=['DELETE'])
def delete_admin(admin_id):
    """删除管理员"""
    pass