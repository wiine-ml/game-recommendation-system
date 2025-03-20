from flask import Blueprint, request, jsonify
from flask_bcrypt import check_password_hash
from ..models import User, Administrator, Developer, Publisher,SUPER_ADMIN, SUPER_ADMIN_PASSWORD
import jwt
from datetime import datetime, timedelta, timezone

login_bp = Blueprint('login_api', __name__)

JWT_SECRET = "GRS2024_ITR3"

@login_bp.route('/api/user/login', methods=['GET','POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('emailOrName')
        password = data.get('password')
        user = User.get_user_by_email(email)
        
        print(user, email, password)
        if not user:
            return jsonify({"msg": "用户不存在", "success": False}), 401

        if not User.check_password(user, password):
            return jsonify({"msg": "密码错误", "success": False}), 401

        token = jwt.encode({
            "user_id": user.id,
            "email": user.email,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }, JWT_SECRET, algorithm="HS256")


        print(user.id, user.username)
        return jsonify({
            "data": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "token": token,
            },
            "msg": "登录成功",
            "success": True
        }), 200

    except Exception as e:
        return jsonify({"msg": str(e), "success": False}), 500


@login_bp.route('/api/admin/login', methods=['GET','POST'])
def admin_login():
    try:
        data = request.get_json()
        admin_name = data.get('emailOrName')
        password = data.get('password')
        # 判断是否是超级管理员登录
        if admin_name == SUPER_ADMIN and password == SUPER_ADMIN_PASSWORD:
            print('!!! super admin login !!!')
            # 超级管理员登录成功，生成令牌
            token = jwt.encode({
                "admin_id": 0,  # 超级管理员的 ID 可以设置为一个特殊的值，比如 0
                "admin_name": admin_name,
                "admin_type": "superAdmin",
                "exp": datetime.now(timezone.utc) + timedelta(hours=1)
            }, JWT_SECRET, algorithm="HS256")

            return jsonify({
                "admin": {
                    "id": 0,
                    "admin_name": admin_name,
                    "admin_type": "superAdmin"
                },
                "token": token,
                "msg": "登录成功",
                "success": True
            }), 200

        # 普通管理员登录逻辑
        admin = Administrator.get_admin_by_name(admin_name)

        if not admin:
            return jsonify({"msg": "管理员不存在", "success": False}), 401

        if not Administrator.check_password(admin, password):
            return jsonify({"msg": "密码错误", "success": False}), 401

        token = jwt.encode({
            "admin_id": admin.id,
            "admin_name": admin.admin_name,
            "admin_type": admin.admin_type,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }, JWT_SECRET, algorithm="HS256")

        return jsonify({
            "admin": {
                "id": admin.id,
                "admin_name": admin.admin_name,
                "admin_type": admin.admin_type
            },
            "token": token,
            "msg": "登录成功",
            "success": True
        }), 200

    except Exception as e:
        return jsonify({"msg": str(e), "success": False}), 500
    
@login_bp.route('/api/vendor/login', methods=['POST'])
def vendor_login():
    try:
        data = request.get_json()
        vendor_name = data.get('emailOrName')
        password = data.get('password')

        # 解析用户名后缀
        parts = vendor_name.split(':')
        if len(parts) < 2:
            return jsonify({
                "data": {},
                "msg": "用户名格式错误，缺少类型后缀",
                "success": False
            }), 400

        username_part = ':'.join(parts[:-1])
        vendor_type = parts[-1].lower()


        # 根据类型查询厂商
        if vendor_type == 'developer':
            vendor = Developer.query.filter_by(DeveloperName=username_part).first()
            password_field = 'DeveloperPassword'
            avatar_field = 'DeveloperAvatar'
        elif vendor_type == 'publisher':
            vendor = Publisher.query.filter_by(PublisherName=username_part).first()
            password_field = 'PublisherPassword'
            avatar_field = 'PublisherAvatar'
        else:
            return jsonify({
                "data": {},
                "msg": "不支持的厂商类型",
                "success": False
            }), 400

        if not vendor:
            return jsonify({
                "data": {},
                "msg": "厂商不存在",
                "success": False
            }), 404

        # 验证密码
        stored_password = getattr(vendor, password_field, None)
        if not stored_password or not check_password_hash(stored_password, password):
            return jsonify({
                "data": {},
                "msg": "密码错误", 
                "success": False
            }), 401

        # 生成JWT令牌
        token_payload = {
            "vendor_id": getattr(vendor, 'DeveloperID' if vendor_type == 'developer' else 'PublisherID'),
            "vendor_name": username_part,
            "vendor_type": vendor_type,
            "exp": datetime.now(timezone.utc) + timedelta(hours=1)
        }
        token = jwt.encode(token_payload, JWT_SECRET, algorithm="HS256")

        return jsonify({
            "data": {
                "token": token,
                "vendor": {
                    "id": token_payload["vendor_id"],
                    "vendor_name": username_part,
                    "vendor_type": vendor_type,
                    "vendor_avatar": getattr(vendor, avatar_field),
                    "vendor_profile": vendor.DeveloperProfile if vendor_type == 'developer' else vendor.PublisherProfile,
                    "vendor_website": vendor.DeveloperWebsite if vendor_type == 'developer' else vendor.PublisherWebsite,
                    "address": vendor.Address,
                    "contact_email": vendor.ContactEmail,
                    "founded_year": vendor.FoundedYear
                }
            },
            "msg": "登录成功",
            "success": True
        }), 200

    except Exception as e:
        return jsonify({
            "data": {},
            "msg": str(e),
            "success": False
        }), 500