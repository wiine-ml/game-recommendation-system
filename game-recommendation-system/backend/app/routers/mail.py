from flask import Blueprint, request, jsonify
from ..models import Mail, User, Developer, Publisher, Administrator
from database import db

str_model_map = {
    'user': User,
    'developer': Developer,
    'publisher': Publisher,
    'administrator': Administrator,
}

mail_bp = Blueprint('mail_api', __name__)

@mail_bp.route('/api/mail/send', methods=['POST'])
def send_mail():
    '''发送邮件'''
    data = request.get_json()
    print(data)
    sender_type = data['sender_type']
    sender_id = data['sender_id']
    receiver_type = data['receiver_type']
    receiver_id = data['receiver_id']
    message = data['message']

    # 检查sender_type和receiver_type是否在str_model_map中
    if sender_type not in str_model_map or receiver_type not in str_model_map:
        response = {
            "data": {},
            "msg": '无效的类型',
            "success": False
        }
        return jsonify(response), 400

    # 检查sender_id对应的用户是否存在
    sender_model = str_model_map[sender_type]
    sender = sender_model.query.filter_by(id=sender_id).first()
    if not sender:
        response = {
            "data": {},
            "msg": '发送者不存在',
            "success": False
        }
        return jsonify(response), 400

    # 检查receiver_id对应的用户是否存在
    receiver_model = str_model_map[receiver_type]
    receiver = receiver_model.query.filter_by(id=receiver_id).first()
    if not receiver:
        response = {
            "data": {},
            "msg": '接收者不存在',
            "success": False
        }
        return jsonify(response), 400

    # 创建Mail对象
    new_mail = Mail(sender_type, sender_id, receiver_type, receiver_id, message)
    new_mail.save()

    response = {
        "data": {},
        "msg": '邮件发送成功',
        "success": True
    }
    return jsonify(response), 200

@mail_bp.route('/api/mail/read/page/<int:page>', methods=['GET'])
def get_mail_paginated(page):
    '''获取邮件分页列表'''
    receiver_type = request.args.get('receiver_type')
    receiver_id = request.args.get('receiver_id')

    print(receiver_type, receiver_id)

    # 检查receiver_type是否在str_model_map中
    if receiver_type not in str_model_map:
        response = {
            "data": {},
            "msg": '无效的类型',
            "success": False
        }
        return jsonify(response), 400

    # 检查receiver_id对应的用户是否存在
    receiver_model = str_model_map[receiver_type]
    receiver = receiver_model.query.filter_by(id=receiver_id).first()
    if not receiver:
        response = {
            "data": {},
            "msg": '接收者不存在',
            "success": False
        }
        return jsonify(response), 400

    # 分页查询邮件
    per_page = 10  # 每页显示的邮件数量
    mails = Mail.query.filter_by(receiverType=receiver_type, receiverID=receiver_id).paginate(page=page, per_page=per_page, error_out=False)

    # 构造返回数据
    mail_list = []
    for mail in mails.items:
        mail_data = {
            'id': mail.id,
            'sender_type': mail.senderType,
            'sender_id': mail.senderID,
            'receiver_type': mail.receiverType,
            'receiver_id': mail.receiverID,
            'message': mail.msgContent
        }
        mail_list.append(mail_data)

    response = {
        "data": {
            'mails': mail_list,
            'current_page': mails.page,
            'total_pages': mails.pages,
            'total_items': mails.total
        },
        "msg": '获取邮件分页列表成功',
        "success": True
    }
    return jsonify(response), 200

@mail_bp.route('/api/mail/delete/<int:mail_id>', methods=['DELETE'])
def delete_mail(mail_id):
    '''删除邮件'''
    data = request.get_json()
    client_type = data['type']
    client_id = data['id']

    # 检查client_type是否在str_model_map中
    if client_type not in str_model_map:
        response = {
            "data": {},
            "msg": '无效的类型',
            "success": False
        }
        return jsonify(response), 400

    # 检查client_id对应的用户是否存在
    client_model = str_model_map[client_type]
    client = client_model.query.filter_by(id=client_id).first()
    if not client:
        response = {
            "data": {},
            "msg": '用户不存在',
            "success": False
        }
        return jsonify(response), 400

    # 检查邮件是否存在且属于该用户
    mail = Mail.query.filter_by(id=mail_id, receiverType=client_type, receiverID=client_id).first()
    if not mail:
        response = {
            "data": {},
            "msg": '邮件不存在或不属于您',
            "success": False
        }
        return jsonify(response), 400

    # 删除邮件
    db.session.delete(mail)
    db.session.commit()

    response = {
        "data": {},
        "msg": '邮件删除成功',
        "success": True
    }
    return jsonify(response), 200