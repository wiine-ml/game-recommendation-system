from datetime import datetime
from sqlalchemy import text
from database import db

class Notice(db.Model):
    __tablename__ = 'notices'

    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(256), nullable=True, default='/admin.jpg')
    username = db.Column(db.String(64), nullable=False)
    title = db.Column(db.String(256), nullable=False, unique=True)
    content = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, id, avatar, username, title, content, date=None):
        self.id = id
        self.avatar = avatar
        self.username = username
        self.title = title
        self.content = content
        if date:
            self.date = date

    def __repr__(self):
        return f"<Notice {self.id}: {self.title}>"

    @staticmethod
    def get_next_id():
        """获取下一个可用的编号"""
        result = db.session.execute(text("SELECT MAX(id) FROM notices"))
        max_id = result.scalar()
        return max_id + 1 if max_id is not None else 0

    @staticmethod
    def create_notice(avatar, username, title, content, date=None):
        """创建公告"""
        next_id = Notice.get_next_id()
        new_notice = Notice(
            id=next_id,
            avatar=avatar,
            username=username,
            title=title,
            content=content,
            date=date
        )
        db.session.add(new_notice)
        db.session.commit()
        return new_notice

    @staticmethod
    def get_notice_by_id(notice_id):
        """根据编号获取公告"""
        return Notice.query.get(notice_id)

    @staticmethod
    def update_notice(notice_id, avatar=None, username=None, title=None, content=None, date=None):
        """更新公告"""
        notice = Notice.query.get(notice_id)
        if not notice:
            raise ValueError("公告不存在")
        if avatar is not None:
            notice.avatar = avatar
        if username is not None:
            notice.username = username
        if title is not None:
            notice.title = title
        if content is not None:
            notice.content = content
        if date is not None:
            notice.date = date
        db.session.commit()
        return notice

    @staticmethod
    def delete_notice(notice_id):
        """删除公告"""
        notice = Notice.query.get(notice_id)
        if not notice:
            raise ValueError("公告不存在")
        db.session.delete(notice)
        db.session.commit()

    # 添加一个方法将对象转换为字典
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'content': self.content,
            'username': self.username,
            # 添加其他需要的字段
        }