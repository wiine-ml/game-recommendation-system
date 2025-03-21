from flask import Blueprint, request, jsonify, send_file
import os
from ..models import User, Interaction, Developer, Publisher
from database import db

vendor_home_page_bp = Blueprint('vendor_home_page_api', __name__)

def get_vendor_model(vendor_type, vendor_id):
    if vendor_type == 'developer':
        return Developer.get_developer_by_id(vendor_id)
    elif vendor_type == 'publisher':
        return Publisher.get_publisher_by_id(vendor_id)
    return None

@vendor_home_page_bp.route('/api/vendor/avatar/read', methods=['GET'])
def read_vendor_avatar():
    """获取厂商头像"""
    vendor_id = request.args.get('vendor_id')
    vendor_type = request.args.get('vendor_type')
    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400
    
    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor.DeveloperAvatar or vendor.DeveloperAvatar == '':
            avatar_filename = "defaultAdmin.jpg"
        else: 
            avatar_filename = vendor.DeveloperAvatar
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor.PublisherAvatar or vendor.PublisherAvatar == '':
            avatar_filename = "defaultAdmin.jpg"
        else: 
            avatar_filename = vendor.PublisherAvatar
        
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
            }), 400

    if not vendor:
        return jsonify({"error": "厂商不存在"}), 404
    
    avatar_path = os.path.join('images', 'vendor_img', 'avatar', avatar_filename)
    print('头像路径：'+ avatar_path)
    if not os.path.exists(avatar_path):
        return jsonify({"error": "头像文件不存在"}), 404
    
    return send_file(avatar_path, mimetype='image/jpeg')

@vendor_home_page_bp.route('/api/vendor/head_image/read', methods=['GET'])
def read_vendor_head_image():
    """获取厂商头图"""
    vendor_id = request.args.get('vendor_id')
    vendor_type = request.args.get('vendor_type')
    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400
    
    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor.DeveloperHeadIllustrations or vendor.DeveloperHeadIllustrations == '':
            head_image_filename = "default_head_image.jpg"
        else: 
            head_image_filename = vendor.DeveloperHeadIllustrations
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor.PublisherHeadIllstration or vendor.PublisherHeadIllstration == '':
            head_image_filename = "default_head_image.jpg"
        else: 
            head_image_filename = vendor.PublisherHeadIllstration
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
        }), 400

    if not vendor:
        return jsonify({"error": "厂商不存在"}), 404
    
    head_image_path = os.path.join('images', 'vendor_img', 'head_img', head_image_filename)
    print('头图路径：' + head_image_path)
    if not os.path.exists(head_image_path):
        return jsonify({"error": "头图文件不存在"}), 404
    
    return send_file(head_image_path, mimetype='image/jpeg')

@vendor_home_page_bp.route('/vendor/prmot_games/read', methods=['GET'])
def read_vendor_promoted_games():
    pass

@vendor_home_page_bp.route('/api/vendor/head_image/upload', methods=['POST'])
def upload_vendor_head_image():
    """上传厂商头图"""
    vendor_id = request.form.get('vendor_id')
    vendor_type = request.form.get('vendor_type')
    file = request.files.get('file')

    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400
    if not file:
        return jsonify({"error": "未上传文件"}), 400

    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "开发商不存在"}), 404
        # 如果已有头图，先删除旧文件
        if vendor.DeveloperHeadIllustrations and vendor.DeveloperHeadIllustrations != '':
            old_head_image_path = os.path.join('images', 'vendor_img', 'head_img', vendor.DeveloperHeadIllustrations)
            if os.path.exists(old_head_image_path):
                os.remove(old_head_image_path)
        # 保存新文件
        filename = f"developer_{vendor_id}_head_image.{file.filename.split('.')[-1]}"
        head_image_path = os.path.join('images', 'vendor_img', 'head_img', filename)
        file.save(head_image_path)
        # 更新数据库
        vendor.DeveloperHeadIllustrations = filename
        db.session.commit()
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "发行商不存在"}), 404
        # 如果已有头图，先删除旧文件
        if vendor.PublisherHeadIllstration and vendor.PublisherHeadIllstration != '':
            old_head_image_path = os.path.join('images', 'vendor_img', 'head_img', vendor.PublisherHeadIllstration)
            if os.path.exists(old_head_image_path):
                os.remove(old_head_image_path)
        # 保存新文件
        filename = f"publisher_{vendor_id}_head_image.{file.filename.split('.')[-1]}"
        head_image_path = os.path.join('images', 'vendor_img', 'head_img', filename)
        file.save(head_image_path)
        # 更新数据库
        vendor.PublisherHeadIllstration = filename
        db.session.commit()
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
        }), 400

    return jsonify({"msg": "头图上传成功", "success": True}), 200

@vendor_home_page_bp.route('/api/vendor/head_image/update', methods=['PUT'])
def update_vendor_head_image():
    """更新厂商头图"""
    vendor_id = request.form.get('vendor_id')
    vendor_type = request.form.get('vendor_type')
    file = request.files.get('file')

    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400
    if not file:
        return jsonify({"error": "未上传文件"}), 400

    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "开发商不存在"}), 404
        # 如果已有头图，先删除旧文件
        if vendor.DeveloperHeadIllustrations and vendor.DeveloperHeadIllustrations != '':
            old_head_image_path = os.path.join('images', 'vendor_img', 'head_img', vendor.DeveloperHeadIllustrations)
            if os.path.exists(old_head_image_path):
                os.remove(old_head_image_path)
        # 保存新文件
        filename = f"developer_{vendor_id}_head_image.{file.filename.split('.')[-1]}"
        head_image_path = os.path.join('images', 'vendor_img', 'head_img', filename)
        file.save(head_image_path)
        # 更新数据库
        vendor.DeveloperHeadIllustrations = filename
        db.session.commit()
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "发行商不存在"}), 404
        # 如果已有头图，先删除旧文件
        if vendor.PublisherHeadIllstration and vendor.PublisherHeadIllstration != '':
            old_head_image_path = os.path.join('images', 'vendor_img', 'head_img', vendor.PublisherHeadIllstration)
            if os.path.exists(old_head_image_path):
                os.remove(old_head_image_path)
        # 保存新文件
        filename = f"publisher_{vendor_id}_head_image.{file.filename.split('.')[-1]}"
        head_image_path = os.path.join('images', 'vendor_img', 'head_img', filename)
        file.save(head_image_path)
        # 更新数据库
        vendor.PublisherHeadIllstration = filename
        db.session.commit()
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
        }), 400

    return jsonify({"msg": "头图更新成功", "success": True}), 200

@vendor_home_page_bp.route('/api/vendor/head_image/delete', methods=['DELETE'])
def delete_vendor_head_image():
    """删除厂商头图"""
    vendor_id = request.args.get('vendor_id')
    vendor_type = request.args.get('vendor_type')

    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400

    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "开发商不存在"}), 404
        if vendor.DeveloperHeadIllustrations and vendor.DeveloperHeadIllustrations != '':
            head_image_path = os.path.join('images', 'vendor_img', 'head_img', vendor.DeveloperHeadIllustrations)
            if os.path.exists(head_image_path):
                os.remove(head_image_path)
            vendor.DeveloperHeadIllustrations = ''
            db.session.commit()
        else:
            return jsonify({"error": "开发商没有头图"}), 400
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "发行商不存在"}), 404
        if vendor.PublisherHeadIllstration and vendor.PublisherHeadIllstration != '':
            head_image_path = os.path.join('images', 'vendor_img', 'head_img', vendor.PublisherHeadIllstration)
            if os.path.exists(head_image_path):
                os.remove(head_image_path)
            vendor.PublisherHeadIllstration = ''
            db.session.commit()
        else:
            return jsonify({"error": "发行商没有头图"}), 400
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
        }), 400

    return jsonify({"msg": "头图删除成功", "success": True}), 200

@vendor_home_page_bp.route('/api/vendor/avatar/upload', methods=['POST'])
def upload_vendor_avatar():
    """上传厂商头像"""
    vendor_id = request.form.get('vendor_id')
    vendor_type = request.form.get('vendor_type')
    file = request.files.get('file')

    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400
    if not file:
        return jsonify({"error": "未上传文件"}), 400

    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "开发商不存在"}), 404
        # 如果已有头像，先删除旧文件
        if vendor.DeveloperAvatar and vendor.DeveloperAvatar != '':
            old_avatar_path = os.path.join('images', 'vendor_img', 'avatar', vendor.DeveloperAvatar)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        # 保存新文件
        filename = f"developer_{vendor_id}_avatar.{file.filename.split('.')[-1]}"
        avatar_path = os.path.join('images', 'vendor_img', 'avatar', filename)
        file.save(avatar_path)
        # 更新数据库
        vendor.DeveloperAvatar = filename
        db.session.commit()
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "发行商不存在"}), 404
        # 如果已有头像，先删除旧文件
        if vendor.PublisherAvatar and vendor.PublisherAvatar != '':
            old_avatar_path = os.path.join('images', 'vendor_img', 'avatar', vendor.PublisherAvatar)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        # 保存新文件
        filename = f"publisher_{vendor_id}_avatar.{file.filename.split('.')[-1]}"
        avatar_path = os.path.join('images', 'vendor_img', 'avatar', filename)
        file.save(avatar_path)
        # 更新数据库
        vendor.PublisherAvatar = filename
        db.session.commit()
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
        }), 400

    return jsonify({"msg": "头像上传成功", "success": True}), 200

@vendor_home_page_bp.route('/api/vendor/avatar/update', methods=['PUT'])
def update_vendor_avatar():
    """更新厂商头像"""
    vendor_id = request.form.get('vendor_id')
    vendor_type = request.form.get('vendor_type')
    file = request.files.get('file')

    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400
    if not file:
        return jsonify({"error": "未上传文件"}), 400

    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "开发商不存在"}), 404
        # 如果已有头像，先删除旧文件
        if vendor.DeveloperAvatar and vendor.DeveloperAvatar != '':
            old_avatar_path = os.path.join('images', 'vendor_img', 'avatar', vendor.DeveloperAvatar)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        # 保存新文件
        filename = f"developer_{vendor_id}_avatar.{file.filename.split('.')[-1]}"
        avatar_path = os.path.join('images', 'vendor_img', 'avatar', filename)
        file.save(avatar_path)
        # 更新数据库
        vendor.DeveloperAvatar = filename
        db.session.commit()
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "发行商不存在"}), 404
        # 如果已有头像，先删除旧文件
        if vendor.PublisherAvatar and vendor.PublisherAvatar != '':
            old_avatar_path = os.path.join('images', 'vendor_img', 'avatar', vendor.PublisherAvatar)
            if os.path.exists(old_avatar_path):
                os.remove(old_avatar_path)
        # 保存新文件
        filename = f"publisher_{vendor_id}_avatar.{file.filename.split('.')[-1]}"
        avatar_path = os.path.join('images', 'vendor_img', 'avatar', filename)
        file.save(avatar_path)
        # 更新数据库
        vendor.PublisherAvatar = filename
        db.session.commit()
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
        }), 400

    return jsonify({"msg": "头像更新成功", "success": True}), 200


@vendor_home_page_bp.route('/api/vendor/avatar/delete', methods=['DELETE'])
def delete_vendor_avatar():
    """删除厂商头像"""
    vendor_id = request.args.get('vendor_id')
    vendor_type = request.args.get('vendor_type')

    if not vendor_id:
        return jsonify({"error": "缺少厂商ID参数"}), 400

    if vendor_type == 'developer':
        vendor = Developer.get_developer_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "开发商不存在"}), 404
        if vendor.DeveloperAvatar and vendor.DeveloperAvatar != '':
            avatar_path = os.path.join('images', 'vendor_img', 'avatar', vendor.DeveloperAvatar)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
            vendor.DeveloperAvatar = ''
            db.session.commit()
        else:
            return jsonify({"error": "开发商没有头像"}), 400
    elif vendor_type == 'publisher':
        vendor = Publisher.get_publisher_by_id(vendor_id)
        if not vendor:
            return jsonify({"error": "发行商不存在"}), 404
        if vendor.PublisherAvatar and vendor.PublisherAvatar != '':
            avatar_path = os.path.join('images', 'vendor_img', 'avatar', vendor.PublisherAvatar)
            if os.path.exists(avatar_path):
                os.remove(avatar_path)
            vendor.PublisherAvatar = ''
            db.session.commit()
        else:
            return jsonify({"error": "发行商没有头像"}), 400
    else:
        return jsonify({
            'data': [],
            "msg": "厂商类型错误",
            'success': False,
        }), 400

    return jsonify({"msg": "头像删除成功", "success": True}), 200