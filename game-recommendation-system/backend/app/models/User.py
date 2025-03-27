from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import text
from PIL import Image
from database import db

import io


class User(db.Model):
    __tablename__ = 'users'

    #用户信息
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    username = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    avatar = db.Column(db.String(255), nullable=True) # 头像路径

    interaction = db.relationship('Interaction', backref='user', lazy=True)

    def __init__(self, email, username, password, avatar_path=None):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password).decode('utf-8')
        self.set_avatar(avatar_path)  # 初始化头像

    def __repr__(self):
        return f"<User {self.username}>"


    @staticmethod
    def add(email, username, password, avatar_path=None):
        """添加用户"""
        user = db.session.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {'email': email}
        ).fetchone()
        if user:
            raise ValueError("邮箱已存在")
        new_user = User(email=email, username=username, password=password, avatar_path=avatar_path)
        db.session.add(new_user)
        db.session.commit()
 
    @staticmethod
    def get_user_by_email(email):
        """根据邮箱获取用户"""
        return db.session.execute(
            text("SELECT * FROM users WHERE email = :email"),
            {'email': email}
        ).fetchone()
    
    @staticmethod
    def get_user_by_id(user_id):
        """根据用户id获取用户"""
        return db.session.query(User).filter_by(id=user_id).first()
    
    @staticmethod
    def check_password(user, password):
        """检查密码是否正确"""
        return check_password_hash(user.password, password)

    def update(self, email=None, username=None, password=None, avatar_path=None):
        """更新用户信息"""
        if email and email != self.email:
            # 使用 execute 检查邮箱是否存在
            existing_user = db.session.execute(
                text("SELECT * FROM users WHERE email = :email"),
                {'email': email}
            ).fetchone()
            if existing_user:
                raise ValueError("邮箱已存在")
            self.email = email
        if username:
            self.username = username
        if password:
            self.password = generate_password_hash(password).decode('utf-8')
        if avatar_path is not None:
            self.set_avatar(avatar_path)  # 更新头像
        db.session.commit()

    def delete(self):
        """删除用户"""
        db.session.delete(self)
        db.session.commit()

    def set_avatar(self, avatar_path):
        """设置头像"""
        self.avatar = avatar_path
        db.session.commit()

    def delete_avatar(self):
        """删除用户头像路径"""
        self.avatar = None
        db.session.commit()